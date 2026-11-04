# Lab 9 — Watching System Calls with `strace`

## Part 1 — `ls -l`

`ls` prints to the terminal with `write`, normally on descriptor **1** (standard output).

The `strace -c -e trace=openat ls -l` run counted **31 `openat` calls**, including **18 errors**. Those errors are failed path lookups during locale and environment setup; they do not mean `ls` failed.

## Part 2 — `syscalls.c`

The first `openat` normally returns descriptor **3** because descriptors **0**, **1**, and **2** are already assigned to standard input, output, and error.

The program opened `note.txt` on descriptor **3**, wrote **14 bytes**, reopened it on descriptor **3**, and read back **14 bytes**: `hello, kernel`. The traced program exited with status **0**.

## Part 3 — Count calls

The handout names this part but does not give its instructions. Using `strace -c -e trace=openat ls -l`, the observed total was **31 `openat` calls**, of which **18** returned errors.
