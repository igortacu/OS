# Lab 8 Observe answers

1. Linux uses fork, execlp/execvp and waitpid. xv6 uses fork, exec and wait. Both create a child, replace its program and collect its status.
2. Echo prints hello from the child after replacing the child copy of run.
3. The explicit fallback exit values are 1 in the xv6 program and 127 in the Linux program.
4. Two pipes give each direction a separate byte stream and prevent competing readers from consuming the wrong message.
5. read(c2p[0], &b, 1) blocks the parent until the reply arrives. The later wait call collects the child.
