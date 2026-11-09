#!/usr/bin/env python3
"""Apply the submitted patch to a clean, disposable xv6 checkout and boot both checks."""
from pathlib import Path
import os, select, subprocess, sys, time
BASE='e93dabeb98431235c6e1a101cb96c73c923fdbc4'
repo=Path(sys.argv[1]).resolve(); patch=Path(sys.argv[2]).resolve()
os.chdir(repo)
def run(*args):
    print('$ '+' '.join(map(str,args)),flush=True)
    subprocess.run(args,check=True)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE
assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip(), 'Use a clean disposable checkout'
print('Verified clean MIT base '+BASE,flush=True)
run('git','apply','--check',str(patch))
run('git','apply',str(patch))
run('git','diff','--check')
source=Path('kernel/syscall.c');complete=source.read_text()
entry='  [SYS_trace] = sys_trace,\n'
assert complete.count(entry)==1

def boot(commands):
    run('make','-j2','kernel/kernel','fs.img')
    p=subprocess.Popen(['make','qemu','CPUS=1'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    def prompt():
        data=bytearray();end=time.monotonic()+120
        while time.monotonic()<end:
            if select.select([p.stdout],[],[],.2)[0]:
                b=os.read(p.stdout.fileno(),65536)
                if not b:raise RuntimeError('QEMU closed')
                data.extend(b)
                if data.endswith(b'$ '):
                    s=data.decode(errors='replace').replace('\r','');print(s,flush=True);return s
        raise RuntimeError('QEMU prompt timeout')
    try:
        prompt();out=''
        for command in commands:
            p.stdin.write((command+'\n').encode());p.stdin.flush();out+=prompt()
        return out
    finally:
        p.stdin.write(b'\x01x');p.stdin.flush();p.wait(timeout=15)
try:
    print('\nCHECK 1: deliberate intermediate build with dispatch registration absent',flush=True)
    source.write_text(complete.replace(entry,''))
    control=boot(['trace 32 grep hello README'])
    assert 'unknown sys call 23' in control and 'trace: failed' in control
finally:
    source.write_text(complete)
print('\nCHECK 2: final submitted patch, registration restored',flush=True)
result=boot(['trace 32 grep hello README','trace 2129920 grep hello README','trace 2 usertests forkforkfork'])
assert 'syscall read ->' in result and 'syscall open ->' in result and 'syscall close ->' in result
assert 'ALL TESTS PASSED' in result and 'unknown sys call' not in result
print('PASS: patch applies; both builds compile; Check 1 reproduces error; final read/open/close and fork inheritance pass',flush=True)
