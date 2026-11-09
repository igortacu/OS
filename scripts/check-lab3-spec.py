#!/usr/bin/env python3
"""Write each prediction before executing the original Lab 3 command."""
from pathlib import Path
import datetime
import json
import os
import subprocess
import tempfile

root=Path(__file__).resolve().parents[1]
work=Path(tempfile.mkdtemp(prefix='igor-lab3-predict-'))
for name in ['a.c','b.c','file1.txt','file2.txt','notes.txt','alfa beta.txt']:
  (work/name).touch()
(root/'Lab3-4/evidence/play-files.txt').write_text(subprocess.check_output(['ls','-1'],cwd=work,text=True))
cases=[
 ('echo *.c','a.c b.c'),
 ('echo file?.txt','file1.txt file2.txt'),
 ('echo [a-b]*','a.c alfa beta.txt b.c'),
 ('echo *.xyz','literal *.xyz because no match exists'),
 ('ls alfa beta.txt','two missing operands and a nonzero status'),
 ('ls "alfa beta.txt"','one file named alfa beta.txt'),
 ("echo '$HOME' \"$HOME\" \\$HOME",'$HOME '+os.environ['HOME']+' $HOME'),
 ('echo {1..5} ; echo $((7 * 6))','1 2 3 4 5 then 42'),
 ('echo "today is $(date +%A), I am $(whoami)"','current weekday and current login identity'),
 ('touch log{1..3}.txt && ls log*','log1.txt, log2.txt, log3.txt'),
]
events=[]
log=root/'Lab3-4/evidence/predictions.json'
for command,prediction in cases:
  event={'command':command,'prediction':prediction,'predicted_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  events.append(event)
  log.write_text(json.dumps(events,indent=2))
  result=subprocess.run(['bash','--noprofile','--norc','-c',command],cwd=work,env={**os.environ,'LC_ALL':'C'},text=True,capture_output=True)
  event.update(stdout=result.stdout,stderr=result.stderr,status=result.returncode,observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
  log.write_text(json.dumps(events,indent=2)+'\n')

comparison=Path(tempfile.mkdtemp(prefix='igor-lab4-compare-'))
(comparison/'README').touch()
commands=['echo hello > f ; cat < f','ls | grep READ','(echo a; echo b) | wc','echo one ; echo two','echo bg &','ls *','echo $HOME','echo "a b"','mkdir d ; cd d ; ls ..']
out=[]
for command in commands:
  result=subprocess.run(['bash','--noprofile','--norc','-c',command],cwd=comparison,text=True,capture_output=True)
  out.append('$ '+command+'\n'+result.stdout+result.stderr)
(root/'Lab3-4/evidence/bash-comparison.txt').write_text(''.join(out))
strict = r'''
set -x
type cd; type ls; type echo; which ls
echo "$PATH"
printf 'PATH directory count: '; echo "$PATH" | awk -F: '{print NF}'
echo "$PATH" | tr ':' '\n'
nosuchprog; echo "exit code: $?"
ls --help | head
man ls | col -b | grep -A2 -- 'sort by modification time' | head -3
man -k 'list directory' | head -3
help cd | head -10
for i in $(seq 1 500); do
  echo "2026-10-05 10:$(printf %02d $((i % 60))) user$((i % 7)) $([ $((i % 5)) -eq 0 ] && echo FAIL || echo OK) /page$((i % 4))"
done > access.log
head -3 access.log; wc -l access.log
ls /etc /nope > out.txt 2> err.txt
wc -l out.txt; cat err.txt
ls /etc /nope > all.txt 2>&1; tail -2 all.txt
ls /etc /nope 2>&1 > all.txt; tail -2 all.txt
echo first > notes.md; echo second >> notes.md; cat notes.md
wc -l < access.log
wc -l access.log
ls /nope 2>/dev/null || echo "failed with code $?"
mkdir -p tmp && cd tmp && echo "I am in $(pwd)"; cd ..
false; echo 'semicolon continues'
false && echo 'not reached'
false || echo 'OR fallback'
sleep 100 &
jobpid=$!
jobs
kill "$jobpid"
wait "$jobpid"
echo "job status: $?"
jobs
cp "$REPO/Lab3-4/linux/oneliners.sh" .
cp "$REPO/Lab3-4/linux/report.sh" .
chmod 644 report.sh
./report.sh access.log
echo "before chmod status: $?"
chmod +x report.sh
./report.sh access.log
./report.sh nope.log; echo "exit code: $?"
bash oneliners.sh
'''
result=subprocess.run(['bash','--noprofile','--norc','-c',strict],cwd=work,env={**os.environ,'LC_ALL':'C','REPO':str(root)},text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(root/'Lab3-4/evidence/handout-linux.txt').write_text(result.stdout)
assert '500 requests, 100 failed' in result.stdout
assert 'before chmod status: 126' in result.stdout
print('PASS original command prediction records and Bash comparison')
