# Lab 17 — native Terminal captures

The actual sources and compiled programs are in `/root/os-lab17` on the Ubuntu
server. Run each block in the SSH terminal and take a screenshot of the real
commands and output. Counters will differ from the recorded experiments.
The current report includes actual text evidence; native screenshots are pending.

## 1. Build and two threads

```bash
cd /root/os-lab17
clear
pwd
make clean all
for i in 1 2 3; do ./fire; done
```

## 2. Four threads

```bash
clear
for i in 1 2 3; do ./fire4; done
```

## 3. Shared variable and unprotected increment

```bash
clear
sed -n '8,25p' fire.c
grep -nE 'pthread_create|pthread_join|THREADS' fire.c
cat Makefile
```

Keep the genuine results even if a run happens to reach the expected total.
There is no guarantee that a C data race always loses updates. Send the native
captures to have them embedded in the UTM report with observations.
