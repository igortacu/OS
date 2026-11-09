#!/usr/bin/env python3
"""Exercise readline completion and reverse history search in a real PTY."""
import os
from pathlib import Path
import pty
import select
import time

root = Path(__file__).resolve().parents[1]
pid, fd = pty.fork()
if pid == 0:
    os.environ.update(TERM='dumb', PS1='igor-bash$ ', HISTFILE='/dev/null')
    os.execlp('bash', 'bash', '--noprofile', '--norc', '-i')

output = bytearray()
def drain(seconds=0.5):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        ready, _, _ = select.select([fd], [], [], 0.05)
        if ready:
            try: output.extend(os.read(fd, 65536))
            except OSError: break

drain()
for data in [b'cd /usr/sh\t', b'\n', b'pwd\n', b'echo history-marker\n', b'\x12pwd\r', b'\n']:
    os.write(fd, data)
    drain()
os.write(fd, b'exit\n')
drain()
for _ in range(30):
    if os.waitpid(pid, os.WNOHANG)[0]: break
    drain(0.1)
else:
    os.kill(pid, 9)
    os.waitpid(pid, 0)
text = output.decode(errors='replace').replace('\r', '')
(root/'Lab3-4/evidence/interactive-bash.txt').write_text(text)
assert '/usr/share' in text
assert 'reverse-i-search' in text
assert text.count('\n/usr/share\n') >= 2
print('PASS completion and reverse history search in Bash PTY')
