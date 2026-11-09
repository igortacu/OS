#!/usr/bin/env python3
"""Build revised reports from authored analysis and committed execution logs."""
from pathlib import Path
import subprocess
import tempfile
import re

ROOT = Path(__file__).resolve().parents[1]
def read(name): return (ROOT/name).read_text()
def segment(text, start, end=None):
    part = text[text.index(start):]
    return part[:part.index(end)].strip() if end else part.strip()

l3, l4 = read('Lab3-4/evidence/linux.txt'), read('Lab3-4/evidence/xv6.txt')
l6 = read('Lab5-6/evidence/xv6.txt')
l5 = read('Lab5-6/evidence/linux.txt')
l7, l8 = read('Lab7-8/evidence/linux.txt'), read('Lab7-8/evidence/xv6.txt')
l9, l10 = read('Lab9-10/evidence/linux.txt'), read('Lab9-10/evidence/xv6.txt')
values = {
 'L3_STATS': segment(l3, 'Q1 failed requests\n', '+ bash '),
 'L4_ARGS': segment(l4, '$ args *.c', '$ echo hello'),
 'L4_SLEEP': segment(l4, '$ sleep 2', '$ args one'),
 'L6_LINKS': segment(l6, '$ echo igor-file', '$ mkdir tree'),
 'L6_FIND': segment(l6, '$ mkdir tree'),
 'L6_EMPTY': segment(l6, '$ mkdir a\n', '$ mystat README'),
 'L6_README': segment(l6, '$ mystat README . console', '$ ln r2 README'),
 'L6_INODE': re.search(r'specimen: type=file inode=(\d+)',l6).group(1),
 'L6_LIMITS': '\n'.join(line for line in read('Lab5-6/evidence/limits.txt').splitlines() if re.match(r'\d+:#define|nmeta',line))+'\n'+'\n'.join(line for line in segment(l6, '$ mkdir averyveryverylongname', '$ mkdir a/b').splitlines() if 'avery' in line or line == '$ ls')+'\n[Other listing entries are retained in the full recording.]',
 'L5_ID': segment(l5, '+ whoami', '+ ls /\n'),
 'L5_TYPES': segment(l5, '+ ls -ld /etc', '+ echo hello'),
 'L5_LINKS': segment(l5, '+ ln notes.txt', '+ mkdir d\n'),
 'L5_PERMS': segment(l5, '+ chmod 600', '+ ls -l /usr/bin/passwd'),
 'L5_DISK': segment(l5, '+ lsblk', '+ grep -c processor'),
 'L7_RUN_SOURCE': '\n'.join(read('Lab7-8/linux/run.c').splitlines()[15:39]),
 'L7_ZOMBIE_SOURCE': '\n'.join(read('Lab7-8/linux/zombie.c').splitlines()[14:32]),
 'L7_REDIRECT_SOURCE': '\n'.join(read('Lab7-8/linux/redirect.c').splitlines()[14:31]),
 'L7_PIPELINE_SOURCE': '\n'.join(read('Lab7-8/linux/pipeline.c').splitlines()[25:56]),
 'L7_RUN': segment(l7, '+ ./run\n', '+ parent_pid='),
 'L7_ZOMBIE': segment(l7, '+ parent_pid=', '+ ./redirect'),
 'L7_PIPE': segment(l7, '+ ./pipeline\n'),
 'L7_ETC': re.search(r'\+ ./pipeline\n(\d+)',l7).group(1),
 'L8_RUN_SOURCE': read('xv6/user/run.c').strip(),
 'L8_PING_SOURCE': read('xv6/user/pingpong.c').strip(),
 'L8_RUN': segment(l8, '$ run\n', '$ run ls\n') + '\n' + segment(l8, '$ run no_such', '$ pingpong'),
 'L8_PING': segment(l8, '$ pingpong'),
 'L9_LS_WRITE': '\n'.join(s for s in read('Lab9-10/evidence/ls.trace').splitlines() if s.startswith('write(1,')),
 'L9_SIX': segment(l9, 'SIX FILE CALLS\n', '+ printf').split('\n', 2)[2],
 'L9_PROGRAM_WRITE': '\n'.join(s for s in read('Lab9-10/evidence/syscalls.trace').splitlines() if s.startswith('write(1,')),
 'L9_COUNT': segment(l9, 'OPENAT COUNTS\n', '+ cp').split('\n', 2)[2],
 'L9_SOURCE': read('Lab9-10/syscalls.c').strip(),
 'L10_USER_SOURCE': read('xv6/user/trace.c').strip(),
 'L10_HANDLER_SOURCE': segment(read('xv6/kernel/sysproc.c'), 'uint64\nsys_trace(void)'),
 'L10_DISPATCH_SOURCE': segment(read('xv6/kernel/syscall.c'), 'void\nsyscall(void)'),
 'L10_PROC_SOURCE': '\n'.join(read('xv6/kernel/proc.h').splitlines()[-5:])+'\n\n'+ '\n'.join(read('xv6/kernel/proc.c').splitlines()[122:130])+'\n\n'+'\n'.join(read('xv6/kernel/proc.c').splitlines()[286:295]),
 'L10_CHECK1': segment(read('Lab9-10/evidence/trace-patch-validation.txt'), 'trace 32 grep hello README', 'CHECK 2:'),
 'L10_READ': segment(l10, '$ trace 32', '$ trace 2147483647'),
 'L10_MASKS': segment(l10, '$ trace 2147483647', '$ trace 2 usertests'),
 'L10_FORK_END': '\n'.join(l10.splitlines()[-12:]),
}

header = '''---
author: Tacu Igor
lang: en
papersize: a4
geometry: margin=2cm
fontsize: 11pt
colorlinks: true
header-includes:
  - \\usepackage{graphicx}
  - \\usepackage{listings}
  - \\lstset{basicstyle=\\ttfamily\\small,breaklines=true,columns=fullflexible,keepspaces=true}
---

'''
targets = [
 ('lab5', 'Lab5-6', 'Lab5_TacuIgor_FAF-242.pdf'),
 ('lab6', 'Lab5-6', 'Lab6_TacuIgor_FAF-242.pdf'),
 ('lab78', 'Lab7-8', 'Lab7-8_TacuIgor_FAF-242.pdf'),
 ('lab910', 'Lab9-10', 'Lab9-10_TacuIgor_FAF-242.pdf'),
]
with tempfile.TemporaryDirectory(prefix='os-report-parts-') as temp:
    temp=Path(temp)
    for template, folder, name in targets:
        text=read(f'scripts/report-templates/{template}.md')
        for key,value in values.items():text=text.replace('@@'+key+'@@',value)
        if '@@' in text:raise RuntimeError('Unresolved report marker')
        md=ROOT/folder/('report-'+template+'.md' if template in ('lab5','lab6') else 'report.md')
        md.write_text('\n'.join(line.rstrip() for line in (header+text).splitlines()).rstrip()+'\n')
        output=temp/name if template in ('lab5','lab6') else ROOT/folder/name
        subprocess.run(['pandoc',str(md),'--pdf-engine=xelatex','--listings',
                        '--lua-filter',str(ROOT/'scripts/keep-code.lua'),
                        '-V','mainfont=Arial','-o',str(output)],check=True)
        print('built',name)
    subprocess.run(['pdfunite',str(temp/'Lab5_TacuIgor_FAF-242.pdf'),
                    str(temp/'Lab6_TacuIgor_FAF-242.pdf'),
                    str(temp/'joint.pdf')],check=True)
    (ROOT/'Lab5-6/Lab5-6_TacuIgor_FAF-242.pdf').write_bytes((temp/'joint.pdf').read_bytes())
