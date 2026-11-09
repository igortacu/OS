#!/usr/bin/env bash
set -u
repo=$(cd "$(dirname "$0")/.." && pwd)
case_root=$(mktemp -d /tmp/os-revision.XXXXXX)
export LC_ALL=C
export PS4='+ '

(
set -x
uname -sm
bash --version | head -1
mkdir -p "$case_root/l3/play"
cd "$case_root/l3"
for ((i=1;i<=500;i++)); do
    status=OK; ((i % 5 == 0)) && status=FAIL
    printf '2026-10-05 10:%02d user%d %s /page%d\n' "$((i%60))" "$((i%7))" "$status" "$((i%4))"
done > access.log
head -3 access.log
wc -l access.log
type cd ls echo
which ls
command -v ls
printf '%s\n' "$PATH" | tr ':' '\n'
nosuchprog
printf 'missing command status=%d\n' "$?"
ls --help | head -10
man ls | col -b | grep -A2 -- 'sort by modification time' | head -3
man -k 'list directory' | head -5
help cd | head -10
cd play
touch alpha.c beta.c entry1.txt entry2.txt 'two words.txt'
printf '<%s>\n' *.c
printf '<%s>\n' '*.c'
printf '<%s>\n' entry?.txt
printf '<%s>\n' *.absent
printf '%s\n' {2..5} "$((9*7))" '$HOME' "$HOME"
ls 'two words.txt'
ls two words.txt
printf 'unquoted filename status=%d\n' "$?"
cd ..
ls play missing >stdout.txt 2>stderr.txt
printf 'ls status=%d\n' "$?"
cat stdout.txt stderr.txt
ls missing >both.txt 2>&1
cat both.txt
ls missing 2>&1 >only-out.txt
wc -c only-out.txt
false && echo SHOULD_NOT_RUN
false || echo RECOVERED
false; echo SEMICOLON_CONTINUES
sleep 60 &
job_pid=$!
jobs
kill "$job_pid"
wait "$job_pid"
printf 'terminated job status=%d\n' "$?"
bash "$repo/Lab3-4/linux/oneliners.sh" access.log
bash "$repo/Lab3-4/linux/report.sh" access.log
bash "$repo/Lab3-4/linux/report.sh" missing.log
printf 'missing input status=%d\n' "$?"
printf '2026-11-09 12:00 user0 OK /page0\n' >all-ok.log
bash "$repo/Lab3-4/linux/report.sh" all-ok.log
cp "$repo/Lab3-4/linux/report.sh" report.sh
chmod 644 report.sh
./report.sh access.log
printf 'without execute permission status=%d\n' "$?"
chmod +x report.sh
./report.sh access.log
wc -l <access.log
wc -l access.log
echo first > notes.md; echo second >>notes.md; cat notes.md
cp "$repo/Lab3-4/linux/args_linux.c" play/
cd play
gcc -std=c11 -Wall -Wextra -Werror -o args args_linux.c
touch sample.c
touch README
./args one    two three
./args *.c 'x y'
./args "$HOME"
./args '$HOME' "$HOME"
./args 'single quoted'
ls | grep READ
ls *
echo "$HOME"
echo "a b"
echo hello > f; cat <f
(echo alpha; echo beta) | wc
mkdir d; cd d; ls ..
) >"$repo/Lab3-4/evidence/linux.txt" 2>&1

(
set -x
mkdir -p "$case_root/l7"
cd "$case_root/l7"
for name in run zombie redirect pipeline; do
  gcc -std=c11 -Wall -Wextra -Werror -o "$name" "$repo/Lab7-8/linux/$name.c" || exit 1
done
./run
./run date -u +%Y-%m-%d
./run no_such_igor_program
./zombie >/dev/null &
parent_pid=$!
sleep 1
ps -o pid,ppid,stat,cmd --ppid "$parent_pid"
wait "$parent_pid"
ps -o pid,ppid,stat,cmd --ppid "$parent_pid"
./redirect
head -3 out.txt
./pipeline
ls /etc | wc -l
time ./pipeline --delay-eof
# Run the handout's actual missing-close variant as a bounded test.
python3 "$repo/scripts/check-broken-pipeline.py" "$repo"
) >"$repo/Lab7-8/evidence/linux.txt" 2>&1

(
set -x
mkdir -p "$case_root/l9"
cd "$case_root/l9"
gcc -std=c11 -Wall -Wextra -Werror -o syscalls "$repo/Lab9-10/syscalls.c"
strace -o ls.trace -e trace=openat,read,write,close ls -l
printf '\nLS STDOUT WRITE\n'
grep '^write(1,' ls.trace
./syscalls
strace -o syscalls.trace -s 200 -e trace=openat,read,write,close ./syscalls
printf '\nSIX FILE CALLS\n'
awk '/openat.*"note.txt"/ {capture=1} capture {print; n++} n==6 {exit}' syscalls.trace
printf '\nPROGRAM STDOUT WRITE\n'
grep '^write(1,' syscalls.trace
printf '\nOPENAT COUNTS\n'
strace -c -e trace=openat ls -l >/dev/null
cp ls.trace syscalls.trace "$repo/Lab9-10/evidence/"
) >"$repo/Lab9-10/evidence/linux.txt" 2>&1

printf 'Linux evidence saved under %s\n' "$repo"
