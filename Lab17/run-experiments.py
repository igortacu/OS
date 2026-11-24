#!/usr/bin/env python3
"""Record repeated real executions; do not assume a race loses every time."""
from pathlib import Path
import json, platform, re, subprocess
root = Path(__file__).resolve().parent
out = root / 'evidence'
out.mkdir(exist_ok=True)
records = []
with (out / 'execution.txt').open('w') as log:
    def record(s):
        print(s, flush=True)
        log.write(s + '\n')
    record('Host: ' + platform.platform())
    record(subprocess.check_output(['gcc', '--version'], text=True).splitlines()[0])
    record('$ make clean all')
    record(subprocess.check_output(['make', 'clean', 'all'], cwd=root, text=True).strip())
    for threads, name in [(2, 'fire'), (4, 'fire4')]:
        runs = []
        for i in range(10):
            record(f'$ ./{name}  # run {i+1}')
            text = subprocess.check_output([str(root/name)], text=True, timeout=15)
            record(text.rstrip())
            expected = int(re.search(r'expected: (\d+)', text)[1])
            counter = int(re.search(r'^counter: (\d+)', text, re.M)[1])
            starts = re.findall(r'thread (\d+) sees counter = (\d+)', text)
            assert expected == threads * 1000000
            assert sorted(int(i) for i, _ in starts) == list(range(1, threads+1))
            runs.append(dict(run=i+1, counter=counter, expected=expected,
                             lost=expected-counter, starts=starts))
        records.append(dict(threads=threads, runs=runs))
    record('Observed data saved; races are undefined behavior, not a guaranteed numeric bound.')
(out/'results.json').write_text(json.dumps(records, indent=2)+'\n')
