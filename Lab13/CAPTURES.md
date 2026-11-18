# Lab 13 — Native Terminal captures

Two isolated xv6 trees are prepared on Ubuntu. `/root/os-lab13-check1` deliberately omits the three semaphore dispatcher entries. `/root/os-lab13` contains the working implementation. The original `/root/xv6-riscv` is untouched. Only the final source tree is submitted in the repository under `xv6/`; the Check 1 tree can be reproduced with `prepare-check1.py`.

## 1. Check 1 — user calls reach an unregistered kernel

In the Linux SSH shell:

```bash
cd /root/os-lab13-check1
make qemu CPUS=3
```

At the xv6 `$` prompt:

```text
semtest
```

Capture the unknown syscall 24/25 messages and the child line appearing before the parent line. Later output is deliberately unsynchronized. The program also prints `semtest: OK` in this incomplete stage because the handout's utility does not validate return codes; this alone is not a passing Check 2.

Exit QEMU with **Ctrl+A, then X** before the next block.

## 2. Check 2 — working semaphores

Back in Linux:

```bash
cd /root/os-lab13
make qemu CPUS=3
```

At the xv6 prompt:

```text
semtest
```

Capture the parent-before-child order, three alternating ping/pong pairs and `semtest: OK`.

## 3. Two unlocked executions

Stay inside the final xv6 shell:

```text
mix
mix
```

Capture the genuine character interleaving. Do not expect exactly the recorded ordering; whole lines can occur by chance without protection.

## 4. Locked output and supplementary checks

Still inside the final xv6 shell:

```text
mix lock
semcheck
```

Capture ten whole 30-letter lines, plus the supplemental test results. The supplemental tests use separate semaphore IDs and verify invalid parameters, counting, the overflow guard, waking four children, and killing a child blocked in sem_down.

## 5. Kernel source and registration

Exit QEMU with **Ctrl+A, then X**, then in Linux:

```bash
cd /root/os-lab13
clear
grep -n 'SYS_sem_' kernel/syscall.h
grep -n 'SYS_sem_' kernel/syscall.c
sed -n '31,55p' kernel/sem.c
```

Capture the registered numbers, table entries and the sleep/wakeup protocol. The report will also include selectable source snippets and direct links to the complete files.
