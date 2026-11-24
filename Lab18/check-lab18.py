#!/usr/bin/env python3
"""Boot the real xv6 image, verify ten complete cooperative schedules."""
from pathlib import Path
import json, os, re, select, subprocess, sys, time
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
log = (out/'execution.txt').open('w', buffering=1)
def record(text):
    print(text, flush=True)
    log.write(text+'\n')
record('$ make qemu CPUS=3')
p = subprocess.Popen(['make','qemu','CPUS=3'],cwd=root,stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
def prompt():
    data=bytearray();deadline=time.monotonic()+90
    while time.monotonic()<deadline:
        if select.select([p.stdout],[],[],0.2)[0]:
            chunk=os.read(p.stdout.fileno(),65536)
            if not chunk:raise RuntimeError('QEMU exited before prompt')
            data.extend(chunk)
            if data.endswith(b'$ '):
                text=data.decode(errors='replace').replace('\r','')
                record(text)
                return text
    raise RuntimeError('QEMU prompt timeout')
def command(s):
    p.stdin.write((s+'\n').encode());p.stdin.flush()
    text=prompt()
    assert text.startswith(s+'\n')
    return text[len(s)+1:-2].rstrip('\n')
results=[]
try:
    prompt()
    for run in range(10):
        text=command('uthread');lines=text.splitlines()
        expected=[f'thread_{c} started' for c in 'abc']
        expected += [f'thread_{c} {n}' for n in range(100) for c in 'cab']
        expected += [f'thread_{c}: exit after 100' for c in 'cab']
        expected += ['thread_schedule: no runnable threads']
        assert lines==expected, f'run {run+1}: incomplete or incorrect round-robin schedule'
        results.append({'run':run+1,'iterations':{'a':100,'b':100,'c':100},
                        'order':'c,a,b','output_lines':len(lines)})
    text=command('trace 32 grep hello README')
    assert 'syscall read ->' in text and 'unknown sys call' not in text
    record('PASS: ten complete 300-iteration schedules; trace read regression passed.')
finally:
    if p.poll() is None:
        p.stdin.write(b'\x01x');p.stdin.flush();p.wait(timeout=15)
    log.close()
(out/'results.json').write_text(json.dumps({'uthread':results,'trace_read':'PASS'},indent=2)+'\n')
