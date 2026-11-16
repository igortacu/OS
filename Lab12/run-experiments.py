#!/usr/bin/env python3
"""Run the required Linux experiments and validate their observable results."""
from pathlib import Path
import collections
import datetime
import json
import re
import shlex
import subprocess

root = Path(__file__).resolve().parent
(root / 'evidence').mkdir(exist_ok=True)
log = (root / 'evidence/execution.txt').open('w', buffering=1)
results = {}

def say(text):
    print(text, flush=True)
    log.write(text + '\n')

def run(args):
    say('$ ' + shlex.join(args))
    p = subprocess.run(args, cwd=root, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=12)
    say(p.stdout.rstrip())
    say(f'exit code: {p.returncode}')
    return p

say('Lab 12 execution ' + datetime.datetime.now(datetime.timezone.utc).isoformat())
for args in [['uname', '-srmo'], ['gcc', '--version'], ['make', 'clean', 'all', 'variants']]:
    assert run(args).returncode == 0

p = run(['./prodcons'])
assert p.returncode == 0
queue = collections.deque()
puts, takes, maximum = [], [], 0
for line in p.stdout.splitlines():
    m = re.fullmatch(r'\s*(put|take) (\d+) \(in buffer: (\d+)\)', line)
    assert m, line
    action, item, count = m.groups()
    item, count = int(item), int(count)
    if action == 'put':
        queue.append(item)
        puts.append(item)
    else:
        assert queue and queue.popleft() == item
        takes.append(item)
    assert count == len(queue) and 0 <= count <= 4
    maximum = max(maximum, count)
assert puts == takes == list(range(1, 9)) and not queue
results['prodcons'] = {'puts': puts, 'takes': takes, 'maximum': maximum,
                       'final_count': len(queue), 'fifo_check': 'PASS'}
(root / 'evidence/prodcons.txt').write_text(p.stdout)

p = run(['timeout', '-k', '1', '5', './variants/prodcons_bad'])
results['prodcons_bad'] = {'exit_code': p.returncode, 'output': p.stdout}
assert p.returncode in (0, 124)

for name in ['condvar', 'variants/condvar_if']:
    p = run(['./' + name])
    assert p.returncode == 0
    lines = p.stdout.splitlines()
    assert lines.count('A: message written') == 1
    assert lines.count('B: I read "hello"') == 1
    assert lines.index('A: message written') < lines.index('B: I read "hello"')
    results[name] = {'exit_code': p.returncode, 'output': p.stdout}

reader_runs = []
for n in range(1, 4):
    p = run(['./readers'])
    assert p.returncode == 0
    writes = re.findall(r'writer (\d+) writes (\d+) \(alone\)', p.stdout)
    reads = re.findall(r'reader (\d+) reads (\d+) \(readers inside: (\d+)\)', p.stdout)
    assert len(writes) == 2 and {int(x[0]) for x in writes} == {1, 2}
    assert [int(x[1]) for x in writes] == [10, 20]
    assert len(reads) == 3 and {int(x[0]) for x in reads} == {1, 2, 3}
    assert all(int(v) in (0, 10, 20) and 1 <= int(c) <= 3 for _, v, c in reads)
    assert 'final value: 20; readers inside: 0' in p.stdout
    reader_runs.append({'output': p.stdout, 'maximum_printed_readers': max(int(x[2]) for x in reads)})
results['readers'] = reader_runs

p = run(['timeout', '-k', '1', '5', './variants/deadlock_bad'])
results['deadlock_bad'] = {'exit_code': p.returncode, 'output': p.stdout}
assert p.returncode in (0, 124)
p = run(['timeout', '-k', '1', '5', './deadlock'])
assert p.returncode == 0 and p.stdout.splitlines()[-1] == 'done'
assert p.stdout.count('I have both') == 2
results['deadlock_fixed'] = {'exit_code': p.returncode, 'output': p.stdout}

codes = []
for i in range(1, 11):
    say(f'Original lock order, no sleeps: run {i}/10')
    p = run(['timeout', '-k', '1', '1', './variants/deadlock_nosleep'])
    assert p.returncode in (0, 124)
    codes.append(p.returncode)
results['deadlock_nosleep'] = {'exit_codes': codes, 'timeout_seconds_per_run': 1}
run(['sha256sum', 'prodcons.c', 'condvar.c', 'readers.c', 'deadlock.c'])
(root / 'evidence/results.json').write_text(json.dumps(results, indent=2) + '\n')
say('PASS: FIFO and occupancy checked for all 16 buffer events; condition publication order checked; reader/writer outputs checked in three runs; fixed lock order completed.')
log.close()
