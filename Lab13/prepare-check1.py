#!/usr/bin/env python3
"""Copy the canonical xv6 source into a NEW disposable Check 1 directory."""
from pathlib import Path
import shutil
import sys

source = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(__file__).resolve().parents[1] / 'xv6'
dest = Path(sys.argv[1]).resolve()
if not (source / 'kernel/syscall.c').is_file() or not (source / 'user/semtest.c').is_file():
    raise SystemExit('Source must be the complete Lab 13 xv6 tree.')
if dest.exists():
    raise SystemExit('Destination already exists; select a new disposable directory.')
shutil.copytree(source, dest, ignore=shutil.ignore_patterns(
    '.git', '*.o', '*.d', '*.asm', '*.sym', '*.img', 'usys.S', '_*'))
for generated in ['kernel/kernel', 'mkfs/mkfs']:
    (dest / generated).unlink(missing_ok=True)
p = dest / 'kernel/syscall.c'
s = p.read_text()
for name in ['sem_init', 'sem_down', 'sem_up']:
    entry = f'  [SYS_{name}] = sys_{name},\n'
    assert s.count(entry) == 1
    s = s.replace(entry, '')
p.write_text(s)
(dest / 'CHECK1.txt').write_text('DELIBERATELY INCOMPLETE dispatch table for Lab 13 Check 1.\n'
                               'Use the separate final tree for the working implementation.\n')
print(f'Prepared disposable Check 1 tree: {dest}')
