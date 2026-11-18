# Lab 13 — Semaphores in Your Own Kernel

Tacu Igor · FAF-242 · Operating Systems · 2026

## Implementation and environment

The canonical modified xv6 tree is [../xv6](../xv6). The three system calls are `sem_init` (24), `sem_down` (25) and `sem_up` (26); the existing `sync` (22) and `trace` (23) remain available. Eight semaphore slots, IDs 0–7, are shared by all processes.

The source was compiled and tested on the Ubuntu server using the RISC-V cross compiler and QEMU with `CPUS=3`. The [final build log](evidence/build-final.txt), [intermediate build log](evidence/build-check1.txt), [QEMU execution log](evidence/execution.txt) and [checked results](evidence/results.json) retain the actual evidence. Tests were performed on 18 November 2026. Both builds complete; their logs retain the linker warnings about RWX LOAD segments in `kernel/kernel` and `user/_forktest`. Intermediate output and final successful output are identified separately.

The implementation follows the Lab 13 handout and this tree's `sleep_prepare(chan)` followed by `sleep()` API. It does not use the older `sleep(chan, lock)` interface. The only canonical kernel tree is committed under `xv6/`; the incomplete Check 1 tree is generated outside the repository by [prepare-check1.py](prepare-check1.py).

## Part 1 — Syscall numbers, declarations and stubs

Registration touches these files:

| File | Role |
| --- | --- |
| [syscall.h](../xv6/kernel/syscall.h) | Reserve numbers 24–26 |
| [user.h](../xv6/user/user.h) | Declare the three user functions |
| [usys.pl](../xv6/user/usys.pl) | Generate the RISC-V ecall stubs |
| [syscall.c](../xv6/kernel/syscall.c) | Declare handlers, register dispatcher entries and trace names |
| [Makefile](../xv6/Makefile) | Link sem.o and put semtest, mix and supplemental semcheck on the disk |

```c
#define SYS_sem_init 24
#define SYS_sem_down 25
#define SYS_sem_up 26

int sem_init(int, int);
int sem_down(int);
int sem_up(int);
```

### Check 1 — deliberately incomplete dispatcher

The disposable `/root/os-lab13-check1` build includes the user stubs but omits all three semaphore handlers from the dispatcher table. The recorded first lines were:

```text
semtest
3 semtest: unknown sys call 24
4 semtest: unknown sys call 25
child: I ran after the parent
parent: done, I let the child go
```

The child did not block because `sem_down` was unrecognized. Subsequent ping/pong text is interleaved with unknown syscall errors. The handout's `semtest` prints `semtest: OK` even at this stage, since it does not check the return values; therefore that final string alone is insufficient evidence of correct semaphores. The validation runner checks the errors and the child-before-parent ordering in Check 1, then checks the entire expected ordered output in Check 2.

## Part 2 — Kernel semaphore operations

Source: [kernel/sem.c](../xv6/kernel/sem.c). Each slot has a protected integer count and a spinlock. The static array begins zeroed, as permitted by the handout's spinlock representation.

`sem_init` rejects IDs outside 0–7 and negative initial values. It replaces the count while holding the slot lock. In these demonstrations, initialization occurs before users begin waiting. The shared table is a teaching interface: it has no ownership, access control, allocation/destruction protocol or FIFO fairness guarantee. Reinitializing an actively used semaphore is outside the experiments and is not a safe reset protocol for existing waiters.

The blocking operation is:

```c
acquire(&s->lock);
while (s->value == 0) {
  sleep_prepare(s);
  release(&s->lock);
  sleep();
  acquire(&s->lock);
  if (killed(myproc())) {
    release(&s->lock);
    return -1;
  }
}
s->value--;
release(&s->lock);
```

Registering the channel while holding the semaphore lock closes the window for a lost semaphore post. If `sem_up` runs after registration but before `sleep`, `wakeup` clears the registered channel and this xv6 implementation's `sleep()` returns without putting the process to sleep. Otherwise the process becomes sleeping and is scheduled away. Once awakened, it reacquires the lock and retries the predicate; it does not busy-poll the count while blocked.

The posting operation, under the same slot lock, is:

```c
if (s->value == 0x7fffffff) {
  release(&s->lock);
  return -1;
}
s->value++;
wakeup(s);
release(&s->lock);
```

The upper-bound check additionally prevents signed integer overflow. The handlers are registered with names in the existing Lab 10 tracer, so tracing a new semaphore call produces its name rather than an absent name entry.

### Check 2 — order and ping/pong

The final implementation passed ten successive executions with this complete sequence:

```text
parent: done, I let the child go
child: I ran after the parent
ping 1
  pong 1
ping 2
  pong 2
ping 3
  pong 3
semtest: OK
```

Semaphore 0 starts at zero. The child waits while the parent pauses for ten ticks; the parent prints before posting the permit. Semaphores 1 and 2 start at one and zero, respectively, and exchange the turn between ping and pong. The runner checks every line and its order in all ten repetitions, not just the final success label.

## Part 3 — Semaphore as a line lock

Source: [user/mix.c](../xv6/user/mix.c).

```c
for (int k = 0; k < 5; k++) {
  if (uselock)
    sem_down(3);
  for (char *p = s; *p; p++)
    write(1, p, 1);
  if (uselock)
    sem_up(3);
}
```

Two unlocked runs were recorded with three QEMU CPUs. Both showed mixed A/b lines; the raw output is preserved without reconstruction in the execution log. The checker verifies a total of 150 `A` characters and 150 `b` characters for each run, so interleaving is distinguished from lost output. Each process emits five newlines as well.

Two locked runs each contained exactly five lines of 30 `A` characters and five lines of 30 `b` characters. In the final saved validation, both locked runs grouped all A lines before all b lines. Scheduling can also switch processes between complete lines. The requirement is: the semaphore protects each complete line, not the entire five-line batch or a prescribed process order.

The required four Observe answers are also provided in [notes.txt](notes.txt):

1. One line costs 31 writes: 30 letters and a newline. Each write is a separate opportunity for the processes to interleave.
2. `sem_down(3)` before the byte loop and `sem_up(3)` after it make the whole line a critical section.
3. `wakeup(s)` can awaken several waiters for one available permit. A competing waiter may consume it first, so the condition must be checked with `while`.
4. The semaphore spinlock must be released before sleeping so a posting process can acquire it and make progress; sleeping with it held also violates the scheduler's spinlock constraints.

## Additional checks and reproduction

The supplemental [user/semcheck.c](../xv6/user/semcheck.c) verifies invalid IDs for all three calls, a negative initial count, the overflow guard, consumption of two permits, release and successful reaping of four waiting children, and killing/reaping a child blocked on a zero-valued semaphore. It reported:

```text
semcheck: bounds and counting OK
semcheck: four waiting children released OK
semcheck: killed blocked child reaped OK
semcheck: OK
```

The finite killed-waiter test exercises an already blocked child; it is not an exhaustive check of every possible kill/sleep interleaving. The handout's wait protocol is retained. The original `trace 32 grep hello README` check and `usertests forkforkfork` also passed after the kernel changes. Tracing syscall 26 with mask 67108864 printed `syscall sem_up -> 0` and allowed semtest to complete. Trace diagnostics can interleave with user output and are retained as recorded.

Build the canonical implementation from `xv6/` with `make kernel/kernel fs.img`, then `make qemu CPUS=3`. To reproduce Check 1, run `python3 Lab13/prepare-check1.py /tmp/os-lab13-check1` from the repository root, build that disposable directory, and keep it separate from the final tree. To repeat automated checks, use `python3 Lab13/check-lab13.py /path/to/final/xv6 /path/to/check1 /path/to/new/evidence`. The checker boots both trees and overwrites the evidence files in its selected output directory.

[Native capture commands](CAPTURES.md) separate the intermediate failure from the final passing implementation. Screenshots will be embedded with captions as the live repetitions are captured; saved command logs are not presented as native live screenshots.
