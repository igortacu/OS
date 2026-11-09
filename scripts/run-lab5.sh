#!/bin/bash
set -u
export LC_ALL=C
if [ "$(id -u)" -eq 0 ]; then
  echo 'Lab 5 must run as an unprivileged user' >&2
  exit 1
fi
work=$(mktemp -d /tmp/igor-lab5.XXXXXX)
cd "$work"
export PS4='+ '
set -x
whoami
id
pwd
ls /
ls -ld /etc /etc/passwd /bin /dev/null /tmp
ls -l /dev | head
file /usr/bin/ls /etc/passwd /bin
readlink -f /bin
find /dev -maxdepth 1 -type c -print | head -1
find /dev -maxdepth 1 -type b -print | head -1
du -sh /var/log 2>/dev/null
du -sh /usr 2>/dev/null
echo hello > notes.txt
stat notes.txt
ls -li notes.txt
ln notes.txt hard.txt
ls -li notes.txt hard.txt
rm notes.txt
cat hard.txt; ls -li hard.txt
ln -s hard.txt soft.txt
ls -li hard.txt soft.txt
cat soft.txt
rm hard.txt
cat soft.txt
printf 'broken symlink cat status=%d\n' "$?"
ls -l soft.txt
mkdir d; ls -ld d
mkdir d/x d/y; ls -ld d
echo x > one.txt; ls -l one.txt; du -h one.txt
truncate -s 1G big.img; ls -lh big.img; du -h big.img
rm big.img
echo secret > s.txt
chmod 600 s.txt; ls -l s.txt
chmod 000 s.txt; cat s.txt
printf 'mode 000 cat status=%d\n' "$?"
chmod u+r s.txt; cat s.txt
umask
touch new.txt; mkdir newdir; ls -ld new.txt newdir
mkdir box; echo hi > box/f
chmod u=r,go= box; ls box; cat box/f
printf 'read-only directory cat status=%d\n' "$?"
chmod u=x,go= box; ls box
printf 'execute-only directory ls status=%d\n' "$?"
cat box/f
chmod 755 box
ls -l /usr/bin/passwd; ls -ld /tmp
if test -r /etc/shadow; then
  echo 'shadow is readable; sensitive contents intentionally not recorded'
else
  cat /etc/shadow
fi
ls -l /etc/shadow
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS
df -h /
findmnt -no SOURCE,FSTYPE,TARGET /
grep -c processor /proc/cpuinfo
head -3 /proc/meminfo
head -5 /proc/self/status
ls -l /proc/self/fd
