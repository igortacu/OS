#!/usr/bin/env python3
"""Put requested source files directly in the original per-lab folders."""
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
def copy(source,target):
    p=ROOT/target;p.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/source,p)

for number in (6,8):
    for name in (['mystat.c','find.c'] if number==6 else ['run.c','pingpong.c']):
        copy('xv6/user/'+name,f'lab{number}/'+name)
    copy('xv6/Makefile',f'lab{number}/Makefile')
for name in ('run','zombie','redirect','pipeline'):
    copy(f'Lab7-8/linux/{name}.c',f'lab7/{name}.c')
copy('Lab3-4/linux/report.sh','lab3/report.sh')
copy('Lab3-4/linux/oneliners.sh','lab3/oneliners.sh')
copy('Lab3-4/linux/args_linux.c','lab4/args_linux.c')
for name in ('args.c','sleep.c'):copy('xv6/user/'+name,'lab4/'+name)
copy('xv6/Makefile','lab4/Makefile')
copy('Lab9-10/syscalls.c','lab9/syscalls.c')
copy('xv6/user/trace.c','lab10/trace.c')
copy('Lab9-10/trace.patch','lab10/trace.patch')
copy('Lab5-6/report-lab5.md','lab5/report.md')
copy('Lab5-6/report-lab6.md','lab6/report.md')
copy('Lab7-8/report.md','lab7/report.md')
copy('Lab7-8/report.md','lab8/report.md')
copy('Lab9-10/report.md','lab9/report.md')
copy('Lab9-10/report.md','lab10/report.md')
notes='''# Lab 8 Observe answers

1. Linux uses fork, execlp/execvp and waitpid. xv6 uses fork, exec and wait. Both create a child, replace its program and collect its status.
2. Echo prints hello from the child after replacing the child copy of run.
3. The explicit fallback exit values are 1 in the xv6 program and 127 in the Linux program.
4. Two pipes give each direction a separate byte stream and prevent competing readers from consuming the wrong message.
5. read(c2p[0], &b, 1) blocks the parent until the reply arrives. The later wait call collects the child.
'''
(ROOT/'lab8/notes.md').write_text(notes)

figs=ROOT/'Lab3-4/evidence/word-figures/browser'
for image in figs.glob('*.jpg'):
    if image.name.startswith(('lab5-','lab6-')):folder='Lab5-6'
    elif image.name.startswith(('lab7-','lab8-')):folder='Lab7-8'
    elif image.name.startswith(('lab9-','lab10-')):folder='Lab9-10'
    else:continue
    copy(str(image.relative_to(ROOT)),folder+'/evidence/screenshots/'+image.name)
print('Packaged source copies and execution screenshots')
