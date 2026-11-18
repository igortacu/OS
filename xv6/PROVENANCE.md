# Source provenance and lab additions

This is a complete source snapshot of the MIT xv6 RISC-V teaching operating system, under the included MIT LICENSE. Upstream: https://github.com/mit-pdos/xv6-riscv . The kernel must not be treated as newly authored student code.

The snapshot starts from the personal fork revision `d3bc70688feb84db11cd2cecf754ad96d6bf6d9c`, based on MIT revision `e93dabeb98431235c6e1a101cb96c73c923fdbc4`. Revision d3bc706 added the Lab 10 trace utility, syscall number and wrapper, dispatcher names and logging, handler, mask initialization, and inheritance. Those files are included here directly so the implementation is reviewable in the OS submission repository.

The November 9 revision adds and tests these user programs:

| Lab | Added source | Purpose |
| --- | --- | --- |
| 4 | `user/args.c`, `user/sleep.c` | Argument arrays and validated tick pause |
| 6 | `user/mystat.c`, `user/find.c` | Metadata and recursive basename search |
| 8 | `user/run.c`, `user/pingpong.c` | Process replacement and two pipes |
| 10 | `user/trace.c` and kernel changes | Per-process syscall tracing |

`Makefile` registers all added programs. Linux experiments are outside this tree under the corresponding lab directories. The build outputs and filesystem image are generated files and are excluded by `.gitignore`.

The November 18 Lab 13 addition implements shared kernel semaphores in
`kernel/sem.c`, registers system calls 24–26 and their user stubs, and adds
`user/semtest.c`, `user/mix.c`, and the supplemental `user/semcheck.c`.
The semaphore implementation and required demonstrations follow the Lab 13
handout, adapted to this tree's two-stage sleep API. `sem_up` additionally
rejects signed count overflow; syscall names are registered for the existing
Lab 10 tracer. The canonical tree retains all earlier lab additions.
