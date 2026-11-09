#!/usr/bin/env python3
"""Boot the committed xv6 tree and save real console output for each lab."""
from pathlib import Path
import os
import select
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT / 'xv6')
# fs.img is a generated test disk. Each run needs a clean fixture namespace.
Path('fs.img').unlink(missing_ok=True)
subprocess.run(['make', '-j2', 'kernel/kernel', 'fs.img'], check=True)
p = subprocess.Popen(['make', 'qemu', 'CPUS=1'], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)

def until_prompt(timeout=90):
    result = bytearray()
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        ready, _, _ = select.select([p.stdout], [], [], 0.2)
        if not ready:
            if p.poll() is not None: raise RuntimeError('QEMU terminated')
            continue
        block = os.read(p.stdout.fileno(), 65536)
        if not block: raise RuntimeError('QEMU output closed')
        result.extend(block)
        if result.endswith(b'$ '): return result.decode(errors='replace').replace('\r', '')
    raise RuntimeError('Timeout waiting for xv6 shell: ' + result.decode(errors='replace')[-1200:])

boot = until_prompt()

def record(relative, commands, checks):
    parts = [boot]
    for command in commands:
        p.stdin.write((command + '\n').encode())
        p.stdin.flush()
        parts.append(until_prompt())
    output = ''.join(parts)
    (ROOT / relative).write_text(output)
    for expected in checks:
        if expected not in output: raise RuntimeError(f'{relative}: missing {expected!r}')
    print('PASS', relative, flush=True)

try:
    record('Lab3-4/evidence/xv6.txt', [
        'sleep 2', 'sleep', 'sleep -1', 'args one    two three',
        'args *.c "x y"', 'args $HOME', "args 'single quoted'",
        'echo hello > l4note; cat < l4note', '(echo alpha; echo beta) | wc',
        'echo first; echo second', 'echo background &',
        'mkdir l4case', 'cd l4case', 'ls', '/ls ..', 'cd /',
    ], ['argc=4', 'argv[1]=[*.c]', 'argv[1]=[$HOME]', 'sleep: invalid tick count', 'exec ls failed'])
    record('Lab5-6/evidence/xv6.txt', [
        'mystat . console', 'echo igor-file > specimen', 'mystat specimen',
        'ln specimen alias', 'mystat specimen alias', 'rm specimen',
        'mystat alias', 'cat alias', 'mystat missing-path',
        'mkdir tree', 'mkdir tree/branch', 'echo root-copy > tree/target',
        'echo nested-copy > tree/branch/target', 'mkdir tree/branch/targetdir',
        'find tree target', 'find tree targetdir', 'find tree branch',
        'echo edge > tree/abcdefghijklmn', 'find tree abcdefghijklmn',
        'find missing-path target', 'find',
    ], ['links=2', 'links=1', 'tree/branch/target', 'tree/branch/targetdir',
        'tree/abcdefghijklmn', 'find: cannot stat missing-path', 'usage: find'])
    record('Lab7-8/evidence/xv6.txt', [
        'run', 'run ls', 'run no_such_igor_program', 'pingpong',
    ], ['hello from the child', 'exec failed', 'status 1', 'received ping', 'received pong'])
    record('Lab9-10/evidence/xv6.txt', [
        'trace 32 grep hello README', 'trace 2147483647 grep hello README',
        'trace 65536 echo hi', 'trace 2129920 grep hello README',
        'trace 2 usertests forkforkfork', 'echo tracing-off',
    ], ['syscall read -> 0', 'syscall write -> 2', 'syscall open -> 3',
        'syscall fork -> -1', 'ALL TESTS PASSED', 'tracing-off'])
finally:
    if p.poll() is None:
        p.stdin.write(b'\x01x')
        p.stdin.flush()
        try: p.wait(timeout=5)
        except subprocess.TimeoutExpired: p.kill()
