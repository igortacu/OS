#!/usr/bin/env python3
"""Run the actual omitted-parent-close case, then interrupt its process group."""
from pathlib import Path
import os
import signal
import subprocess
import sys
import time

repo=Path(sys.argv[1])
source=(repo/'Lab7-8/linux/pipeline.c').read_text()
anchor='    close(p[1]);\n    int ls_status, wc_status;'
assert source.count(anchor)==1
broken=source.replace(anchor,'    /* close(p[1]); intentionally omitted for Part 4.3 */\n    int ls_status, wc_status;')
Path('pipeline_broken.c').write_text(broken)
subprocess.run(['gcc','-Wall','-Wextra','-Werror','-o','pipeline_broken','pipeline_broken.c'],check=True)
p=subprocess.Popen(['./pipeline_broken'],start_new_session=True)
time.sleep(2)
try:
  assert p.poll() is None, 'Broken pipeline unexpectedly terminated'
  print('Part 4.3: pipeline is still running after two seconds',flush=True)
  subprocess.run(['ps','-o','pid,ppid,stat,cmd','--ppid',str(p.pid)],check=True)
finally:
  os.killpg(p.pid,signal.SIGINT)
  p.wait(timeout=5)
print('Interrupted with SIGINT (Ctrl-C equivalent); return code',p.returncode,flush=True)
assert p.returncode == -signal.SIGINT
