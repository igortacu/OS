#!/usr/bin/env python3
"""Build revised reports from authored analysis and committed execution logs."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
def read(name): return (ROOT/name).read_text()
def segment(text, start, end=None):
    part = text[text.index(start):]
    return part[:part.index(end)].strip() if end else part.strip()

l3, l4 = read('Lab3-4/evidence/linux.txt'), read('Lab3-4/evidence/xv6.txt')
l6 = read('Lab5-6/evidence/xv6.txt')
l7, l8 = read('Lab7-8/evidence/linux.txt'), read('Lab7-8/evidence/xv6.txt')
l9, l10 = read('Lab9-10/evidence/linux.txt'), read('Lab9-10/evidence/xv6.txt')
values = {
 'L3_STATS': segment(l3, 'Q1 failed requests\n', '+ bash /work/Lab3-4/linux/report.sh access.log'),
 'L4_ARGS': segment(l4, '$ args *.c', '$ echo hello'),
 'L4_SLEEP': segment(l4, '$ sleep 2', '$ args one'),
 'L6_LINKS': segment(l6, '$ echo igor-file', '$ mkdir tree'),
 'L6_FIND': segment(l6, '$ mkdir tree'),
 'L7_RUN': segment(l7, '+ ./run\n', '+ parent_pid='),
 'L7_ZOMBIE': segment(l7, '+ parent_pid=', '+ ./redirect'),
 'L7_PIPE': segment(l7, '+ ./pipeline\n'),
 'L8_RUN': segment(l8, '$ run\n', '$ run ls\n') + '\n' + segment(l8, '$ run no_such', '$ pingpong'),
 'L8_PING': segment(l8, '$ pingpong'),
 'L9_LS_WRITE': '\n'.join(s for s in read('Lab9-10/evidence/ls.trace').splitlines() if s.startswith('write(1,')),
 'L9_SIX': segment(l9, 'SIX FILE CALLS\n', '+ printf').split('\n', 2)[2],
 'L9_PROGRAM_WRITE': '\n'.join(s for s in read('Lab9-10/evidence/syscalls.trace').splitlines() if s.startswith('write(1,')),
 'L9_COUNT': segment(l9, 'OPENAT COUNTS\n', '+ cp').split('\n', 2)[2],
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
  - \\usepackage{listings}
  - \\lstset{basicstyle=\\ttfamily\\small,breaklines=true,columns=fullflexible,keepspaces=true}
---

'''
targets = [
 ('lab34', 'Lab3-4', 'Lab3-4_TacuIgor_FAF-242.pdf'),
 ('lab6', 'Lab5-6', 'Lab6_TacuIgor_FAF-242.pdf'),
 ('lab78', 'Lab7-8', 'Lab7-8_TacuIgor_FAF-242.pdf'),
 ('lab910', 'Lab9-10', 'Lab9-10_TacuIgor_FAF-242.pdf'),
]
for template, folder, name in targets:
    text = read(f'scripts/report-templates/{template}.md')
    for key, value in values.items(): text = text.replace('@@'+key+'@@', value)
    if '@@' in text: raise RuntimeError('Unresolved report marker')
    md = ROOT/folder/('report-lab6.md' if template == 'lab6' else 'report.md')
    md.write_text('\n'.join(line.rstrip() for line in (header+text).splitlines()).rstrip()+'\n')
    subprocess.run(['pandoc', str(md), '--pdf-engine=xelatex', '--listings',
                    '--lua-filter', str(ROOT/'scripts/keep-code.lua'),
                    '-V', 'mainfont=Arial', '-o', str(ROOT/folder/name)], check=True)
    print('built', folder+'/'+name)

# Preserve the Linux portion of the old joint report and replace its xv6 section.
joint = ROOT/'Lab5-6/Lab5-6_TacuIgor_FAF-242.pdf'
with tempfile.TemporaryDirectory(prefix='lab5-prefix-') as temp:
    subprocess.run(['pdfseparate', '-f', '1', '-l', '8', str(joint), temp+'/page-%d.pdf'], check=True)
    merged = Path(temp)/'merged.pdf'
    subprocess.run(['pdfunite', *[temp+f'/page-{i}.pdf' for i in range(1,9)],
                    str(ROOT/'Lab5-6/Lab6_TacuIgor_FAF-242.pdf'), str(merged)], check=True)
    joint.write_bytes(merged.read_bytes())
