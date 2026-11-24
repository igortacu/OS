# Lab 18 — native Terminal captures

The completed tree is prepared at `/root/os-lab18/xv6` on the Ubuntu server.
It is an isolated copy of the submitted `xv6/`, with all earlier lab additions.
The context/build-rule and complete assembly native captures are embedded in the report. The final execution capture is also embedded. Only the startup/first-rounds native capture is pending; full real QEMU text evidence is already retained.

## 1. Context, initial registers and build rule (Linux)

```bash
cd /root/os-lab18/xv6
clear
sed -n '10,19p' user/uthread.c
grep -n -A5 'memset(&t->ctx' user/uthread.c
tail -n 5 Makefile
make user/_uthread
```

## 2. Save and restore (Linux)

```bash
clear
cat -n user/uthread_switch.S
```

## 3. Execute (xv6)

Start QEMU from Linux:

```bash
make qemu CPUS=3
```

At the xv6 `$` prompt, type only:

```text
uthread
```

Take a screenshot of the final screen showing counts through 99, all three
`exit after 100` messages and `thread_schedule: no runnable threads`.
Use the terminal's scrollback for another capture of the three `started`
messages and the first `c 0 / a 0 / b 0` rounds. Do not type Linux `clear`,
`head` or `tail` inside xv6. The final diagnostic follows the handout's exit(-1)
path after all workers finish; it does not mean a register switch failed.
Exit QEMU using Ctrl+A, then X.

The full ten-run verification is preserved in `evidence/execution.txt` and
`evidence/results.json`; these are real automated executions, not screenshots.
