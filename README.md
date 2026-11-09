# Operating Systems Labs — Tacu Igor, FAF-242

Laboratory work reports for the Operating Systems course (Technical University of Moldova, 2026).

| Labs | Topic | Report |
|------|-------|--------|
| 1 & 2 | The OS as a Resource Manager (Linux + xv6) | [PDF](Lab1-2/Lab1-2_TacuIgor_FAF-242.pdf) |
| 3 & 4 | Bash command line | [PDF](Lab3-4/Lab3-4_TacuIgor_FAF-242.pdf) |
| 5 & 6 | The File System with Your Own Hands | [PDF](Lab5-6/Lab5-6_TacuIgor_FAF-242.pdf) |
| 7 & 8 | Processes, Redirection and a Pipe — the same calls inside your own OS | [PDF](Lab7-8/Lab7-8_TacuIgor_FAF-242.pdf) |
| 9 & 10 | Watching system calls and adding `trace` to xv6 | [PDF](Lab9-10/Lab9-10_TacuIgor_FAF-242.pdf) |

## Source code and evidence

The complete modified [xv6 tree](xv6) is included in this repository. Its [provenance](xv6/PROVENANCE.md) identifies the MIT source and the additions made for these labs.

| Lab | Review these sources | New execution evidence |
| --- | --- | --- |
| 3 | [log pipelines](Lab3-4/linux/oneliners.sh), [report script](Lab3-4/linux/report.sh) | [Linux transcript](Lab3-4/evidence/linux.txt), [completion and history](Lab3-4/evidence/interactive-bash.txt) |
| 4 | [xv6 args](xv6/user/args.c), [xv6 sleep](xv6/user/sleep.c), [Linux args](Lab3-4/linux/args_linux.c) | [xv6 transcript](Lab3-4/evidence/xv6.txt) |
| 6 | [mystat.c](xv6/user/mystat.c), [find.c](xv6/user/find.c) | [metadata and search tests](Lab5-6/evidence/xv6.txt) |
| 7 | [run.c](Lab7-8/linux/run.c), [zombie.c](Lab7-8/linux/zombie.c), [redirect.c](Lab7-8/linux/redirect.c), [pipeline.c](Lab7-8/linux/pipeline.c) | [Linux process tests](Lab7-8/evidence/linux.txt) |
| 8 | [run.c](xv6/user/run.c), [pingpong.c](xv6/user/pingpong.c) | [xv6 process tests](Lab7-8/evidence/xv6.txt) |
| 9 | [syscalls.c](Lab9-10/syscalls.c) | [write on fd 1 and six file calls](Lab9-10/evidence/linux.txt), [complete strace](Lab9-10/evidence/syscalls.trace) |
| 10 | [trace.c](xv6/user/trace.c), [handler](xv6/kernel/sysproc.c), [dispatch](xv6/kernel/syscall.c), [process inheritance](xv6/kernel/proc.c), [mask field](xv6/kernel/proc.h), [number](xv6/kernel/syscall.h), [declaration](xv6/user/user.h), [stub](xv6/user/usys.pl), [registration](xv6/Makefile) | [mask and fork tests](Lab9-10/evidence/xv6.txt), [standalone implementation patch](Lab9-10/trace.patch) |

The [reproduction instructions](scripts/README.md) build a fresh test disk and run the same cases. Revised reports use new November 9 output and case-specific analysis. They do not reuse the previous Labs 3 and 4 screenshots. Lab 5 was rerun as the unprivileged account oslab_igor on the Ubuntu server, including permissions and physical disk observations. Screenshots display the saved SSH execution records in a read-only browser console; they include source excerpts and retain links to the raw transcripts.

The original individual Word submissions are [Lab 3](lab3/Lab3_TacuIgor_FAF-242.docx) and [Lab 4](lab4/Lab4_TacuIgor_FAF-242.docx), with screenshot-inclusive PDF exports [L3](lab3/Lab3_TacuIgor_FAF-242.pdf) and [L4](lab4/Lab4_TacuIgor_FAF-242.pdf). Direct per-lab source folders are [lab6](lab6), [lab7](lab7), [lab8](lab8), [lab9](lab9), and [lab10](lab10). The complete buildable xv6 integration remains in [xv6](xv6).

Lab 10 includes [exact-base patch instructions and verification](Lab9-10/PATCH-VALIDATION.md), including the intentionally incomplete Check 1 and the working final implementation.

Lab 4: all twelve figures in the individual Word/PDF report now use author-supplied native Terminal screenshots of direct execution and source inspection. Originals and their figure mapping are in [native captures](Lab3-4/evidence/word-figures/native/manifest.json). Other labs are being updated separately.

Lab 3: all twenty-four figure references in the individual Word/PDF report now use author-supplied native Terminal screenshots. Adjacent questions may share a capture; the [manifest](Lab3-4/evidence/word-figures/native/manifest.json) records these mappings. Initial prediction records remain separate from the later screenshot runs.
