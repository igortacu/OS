# Operating Systems — Tacu Igor, FAF-242

Each laboratory pair has one main PDF. Reports include native Terminal screenshots, explanations and source excerpts.

| Laboratories | Subject | Main report |
| --- | --- | --- |
| 1–2 | Linux resources and introduction to xv6 | [PDF](Lab1-2/Lab1-2_TacuIgor_FAF-242.pdf) |
| 3–4 | Bash commands, pipelines and the xv6 shell | [PDF](Lab3-4/Lab3-4_TacuIgor_FAF-242.pdf) |
| 5–6 | Linux and xv6 filesystems | [PDF](Lab5-6/Lab5-6_TacuIgor_FAF-242.pdf) |
| 7–8 | Processes, redirection and pipes | [PDF](Lab7-8/Lab7-8_TacuIgor_FAF-242.pdf) |
| 9–10 | Linux strace and the xv6 trace system call | [PDF](Lab9-10/Lab9-10_TacuIgor_FAF-242.pdf) |

Source files and execution evidence:

| Laboratory | Source |
| --- | --- |
| 3 | [oneliners.sh](Lab3-4/linux/oneliners.sh), [report.sh](Lab3-4/linux/report.sh) |
| 4 | [Linux argument inspector](Lab3-4/linux/args_linux.c), [xv6 args](xv6/user/args.c), [xv6 sleep](xv6/user/sleep.c) |
| 6 | [mystat.c](xv6/user/mystat.c), [find.c](xv6/user/find.c) |
| 7 | [run.c](Lab7-8/linux/run.c), [zombie.c](Lab7-8/linux/zombie.c), [redirect.c](Lab7-8/linux/redirect.c), [pipeline.c](Lab7-8/linux/pipeline.c) |
| 8 | [run.c](xv6/user/run.c), [pingpong.c](xv6/user/pingpong.c) |
| 9 | [syscalls.c](Lab9-10/syscalls.c) |
| 10 | [trace.c](xv6/user/trace.c), [handler](xv6/kernel/sysproc.c), [dispatcher](xv6/kernel/syscall.c), [process state](xv6/kernel/proc.h), [inheritance](xv6/kernel/proc.c), [validated patch](Lab9-10/trace.patch) |

The single integrated [xv6 source tree](xv6) includes its MIT license and [provenance](xv6/PROVENANCE.md). Each report folder contains its raw evidence and original screenshots. The two labeled Lab 10 patch-audit captures display saved verification output; final experiment screenshots show direct execution.

The original handouts require individual Word files for Labs 3 and 4; these editable sources are retained under [Lab3-4/word](Lab3-4/word). Their PDF exports are combined into the single main report linked above.

[Reproduction and PDF export instructions](scripts/README.md) · [Lab 10 patch verification](Lab9-10/PATCH-VALIDATION.md)
