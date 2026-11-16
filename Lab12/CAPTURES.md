# Lab 12 — Native Terminal captures

Run each block in the Ubuntu SSH terminal, one at a time. The source and compiled programs have been prepared in `/root/os-lab12`. Capture the actual command and output of each block; scheduling may change the order. Send the screenshots to embed them in the report.

## 1. Build and transfer all eight items

```bash
cd /root/os-lab12
clear
pwd
make clean all
./prodcons
```

## 2. Incorrect producer lock order

```bash
cd /root/os-lab12
clear
make variants
sed -n '18,25p' variants/prodcons_bad.c
timeout -k 1 5 ./variants/prodcons_bad
echo "exit code: $?"
```

## 3. Condition variable and the if variant

```bash
cd /root/os-lab12
clear
grep -nE 'while|pthread_cond_wait|ready = 1|pthread_cond_signal' condvar.c
./condvar
grep -n 'if (!ready)' variants/condvar_if.c
./variants/condvar_if
```

## 4. Readers and writers

```bash
cd /root/os-lab12
clear
sed -n '17,32p' readers.c
./readers
```

## 5. Deadlock and fixed lock order

```bash
cd /root/os-lab12
clear
timeout -k 1 5 ./variants/deadlock_bad
echo "original exit code: $?"
timeout -k 1 5 ./deadlock
echo "fixed exit code: $?"
```

## 6. Original lock order with both sleeps removed

```bash
cd /root/os-lab12
clear
grep -n 'sleep' variants/deadlock_nosleep.c
for i in $(seq 1 10); do
    timeout -k 1 1 ./variants/deadlock_nosleep > /tmp/os-lab12-nosleep-$i.txt 2>&1
    printf 'run %2d: exit code %s\n' "$i" "$?"
done
cat /tmp/os-lab12-nosleep-1.txt
```

The first `grep` should find no sleep calls. A timeout returns 124; a completed run returns 0. Keep whatever results actually occur. Ten timeouts are also a valid observation. The absence of a timeout in some schedules would not fix the lock-order defect.
