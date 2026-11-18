#!/usr/bin/env python3
"""Boot disposable Check 1 and final xv6 trees; save real QEMU output."""
from pathlib import Path
import collections
import json
import os
import select
import subprocess
import sys
import time

final = Path(sys.argv[1]).resolve()
control = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3]).resolve()
out.mkdir(parents=True, exist_ok=True)
results = {}
log = (out / 'execution.txt').open('w', buffering=1)

def record(text):
    print(text, flush=True)
    log.write(text + '\n')

class Machine:
    def __init__(self, tree):
        record(f'$ cd {tree} && make qemu CPUS=3')
        self.p = subprocess.Popen(['make', 'qemu', 'CPUS=3'], cwd=tree,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, bufsize=0)
        self.prompt()

    def prompt(self):
        data = bytearray()
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if select.select([self.p.stdout], [], [], 0.2)[0]:
                chunk = os.read(self.p.stdout.fileno(), 65536)
                if not chunk:
                    raise RuntimeError('QEMU exited before its prompt')
                data.extend(chunk)
                if data.endswith(b'$ '):
                    text = data.decode(errors='replace').replace('\r', '')
                    record(text)
                    return text
        raise RuntimeError('QEMU prompt timeout')

    def command(self, command):
        self.p.stdin.write((command + '\n').encode())
        self.p.stdin.flush()
        text = self.prompt()
        assert text.startswith(command + '\n'), repr(text[:100])
        return text[len(command) + 1:-2].removesuffix('\n')

    def close(self):
        if self.p.poll() is None:
            self.p.stdin.write(b'\x01x')
            self.p.stdin.flush()
            self.p.wait(timeout=15)

record('CHECK 1: semaphore stubs present; all three dispatcher entries absent.')
m = Machine(control)
try:
    text = m.command('semtest')
    assert 'unknown sys call 24' in text and 'unknown sys call 25' in text
    assert text.index('child: I ran after the parent') < text.index('parent: done, I let the child go')
    results['check1'] = text
finally:
    m.close()

record('CHECK 2: final registered semaphore implementation, three QEMU CPUs.')
m = Machine(final)
try:
    expected = ['parent: done, I let the child go', 'child: I ran after the parent',
                'ping 1', 'pong 1', 'ping 2', 'pong 2', 'ping 3', 'pong 3', 'semtest: OK']
    runs = []
    for i in range(10):
        text = m.command('semtest')
        assert [line.strip() for line in text.splitlines()] == expected
        runs.append(text)
    results['semtest'] = {'repetitions': len(runs), 'outputs': runs}
    unlocked = []
    for i in range(2):
        text = m.command('mix')
        assert collections.Counter(text) == collections.Counter({'A': 150, 'b': 150, '\n': 9})
        mixed = sum('A' in line and 'b' in line for line in text.splitlines())
        unlocked.append({'output': text, 'mixed_lines': mixed})
    results['mix_unlocked'] = unlocked
    locked = []
    for i in range(2):
        text = m.command('mix lock')
        assert collections.Counter(text.splitlines()) == collections.Counter({'A' * 30: 5, 'b' * 30: 5})
        locked.append(text)
    results['mix_locked'] = locked
    text = m.command('semcheck')
    assert 'FAIL' not in text and text.endswith('semcheck: OK')
    results['semcheck'] = text
    text = m.command('trace 67108864 semtest')
    assert 'syscall sem_up -> 0' in text and 'unknown sys call' not in text and 'semtest: OK' in text
    results['trace_sem_up'] = text
    text = m.command('trace 32 grep hello README')
    assert 'syscall read ->' in text and 'unknown sys call' not in text
    results['trace_regression'] = text
    text = m.command('usertests forkforkfork')
    assert 'ALL TESTS PASSED' in text
    results['fork_regression'] = text
finally:
    m.close()
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
record('PASS: Check 1; 10 ordered semtest runs; two unlocked and two whole-line locked mix runs; bounds/counting/waiters/kill; trace and fork regressions.')
log.close()
