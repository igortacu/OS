# Processes descriptors and two way communication

Tacu Igor, FAF 242\
Laboratory Works 7 and 8, Operating Systems\
New reproduction on 9 November 2026

## Question and execution environment

A shell pipeline and a child that replaces itself with another program both depend on state that survives process creation or program replacement. Lab 7 isolates that state under Linux: PIDs, wait status, open descriptors, and pipe endpoints. Lab 8 applies the same ideas to xv6, where the user API and kernel implementation are small enough to inspect together. The revised experiments below were run in Ubuntu 24.04 ARM64 on Docker and in QEMU with the committed xv6 source. The output is from the new run, not the earlier SSH screenshots.

All six requested programs are present in this repository. Linux sources are in `Lab7-8/linux`; xv6 sources are `xv6/user/run.c` and `xv6/user/pingpong.c`. The complete xv6 tree includes the UPROGS registrations. Raw transcripts are in `Lab7-8/evidence`, and the two runner scripts under `scripts` retain the commands that produced them.

## Lab 7 Replacing a child while preserving its identity

`run.c` flushes the parent's initial message before calling `fork`. Otherwise buffered output could be copied and later printed twice when stdout is redirected. The child prints its identity, flushes that output, and invokes `execvp` for an explicit command or `execlp` for the default `ls -l`. The parent waits for the particular child PID with `waitpid`, then distinguishes normal exit from signal termination before interpreting the status bits.

The default listing, a UTC date command, and a deliberately absent program exercise three paths. Both successful programs return status zero. The absent executable returns from exec, prints the error, and calls `_exit(127)`. The parent subsequently reports 127 for the child; the parent utility itself returns normally after reporting that result. It would be misleading to describe the parent's own exit code as 127 simply because that number appears in its message.

```text
@@L7_RUN@@
```

Successful exec does not create an additional child and does not run the fallback error branch. It replaces the calling child's address space while retaining its PID and inherited descriptors. This is why the listing appears between the child's identification and the parent's completion message. The exact PID values are incidental; the relationship between them is the part under test.

## Lab 7 Delaying collection of a terminated child

`zombie.c` uses the same exec path but makes the parent sleep before `waitpid`. The child can finish its listing while the parent is still alive. The process query selects children of the saved background parent PID, which avoids mixing this case with unrelated processes on the machine. The first query found a `Z` entry for ls; after waiting for the parent utility, the second query contained only the header.

```text
@@L7_ZOMBIE@@
```

The zombie is not a program still executing the ls instructions. It is the kernel's retained termination information awaiting collection. The delay makes this normally short interval observable. Using `$!` immediately after launching the parent and filtering with `--ppid` ties the observed entry to the experiment rather than to a coincidentally named process.

## Lab 7 Redirecting output by descriptor reuse

The redirection child closes descriptor 1 before opening `out.txt`. Since open chooses the lowest available descriptor, the new descriptor is 1. The later ls image writes through the standard-output number it always uses, but that number now refers to the file. The diagnostic is deliberately written to stderr and remains visible outside the file. The parent waits and checks the child's status before announcing completion.

The run reported `open gave descriptor 1`; reading the first lines of `out.txt` displayed the saved listing. The listing showed `out.txt` as empty at the moment ls inspected its metadata. That does not mean redirection failed: ls is itself in the process of generating the bytes subsequently read by head.

## Lab 7 A pipe whose reader needs every writer to close

`pipeline.c` creates one pipe and two children. The ls child duplicates the write endpoint onto stdout. The wc child duplicates the read endpoint onto stdin. Each child closes both original endpoints after duplication, and the parent also closes its copies before collecting both children. The ordinary program and `ls /etc | wc -l` each returned **116** in this environment. This is a measurement of the current container's `/etc`, not a fixed expected value for Ubuntu.

The revised program includes a bounded `--delay-eof` mode. It retains the parent's write endpoint for three seconds, then closes it. This demonstrates the reader's dependence on the last writer without leaving a permanently blocked process behind. The measured elapsed time was about three seconds, and wc eventually returned the same count.

```text
@@L7_PIPE@@
```

The delay does not make ls produce more directory entries. It postpones the EOF condition that lets wc finish. A pipe read can reach EOF only after buffered bytes have been consumed and every descriptor referring to its write end has been closed. Copies inherited through fork count too, which is why closing endpoints only in the producer is insufficient.

## Lab 8 Reusing the lifecycle inside xv6

The xv6 `run` utility defaults to echo but also accepts a command and its arguments. This makes success and failure reproducible without editing source between each test. It calls fork, uses exec in the child, and waits in the parent. `run` printed `hello from the child` and status zero; `run ls` listed the generated filesystem; `run no_such_igor_program` took the fallback branch and reported status one.

```text
@@L8_RUN@@
```

The Linux fallback uses 127 and the xv6 fallback uses 1 because those values are explicitly chosen by the utilities. Exec failure does not force every program or OS to choose the same status. The xv6 wait API also differs from Linux waitpid: it collects a child and writes the status through a pointer without selecting a particular PID in this program.

## Lab 8 Passing a byte in each direction

`pingpong.c` creates separate parent-to-child and child-to-parent pipes before forking. The parent sends one byte on the first pipe and blocks waiting on the second. The child reads the byte, prints its ping message, and returns the byte on the other pipe. Both processes close the endpoints they do not use; the parent then waits to collect the child. The implementation checks every one-byte read and write instead of assuming a transfer succeeded.

```text
@@L8_PING@@
```

The observed ping-before-pong order follows from the data dependency: the parent cannot print pong until the child's reply is read. A single unstructured pipe would not encode the two directions so clearly and would allow processes to compete for the same stream. Two pipes make both ownership and the blocking points explicit.

## Interpretation and source provenance

These tests connect shell behavior to specific lifetime rules. Fork copies descriptor references, exec preserves them, wait collects termination state, and close can determine whether another process is allowed to finish. The delayed EOF experiment is particularly useful because its final count is unchanged while its completion time changes. It distinguishes a communication-lifetime error from an incorrect data-processing result.

The runner checks compilation with `-Wall -Wextra -Werror`, verifies the Linux cases, builds the complete xv6 image, and checks distinctive output for run and pingpong. It does not claim that this limited set proves arbitrary error recovery or all scheduling orders. MIT xv6 remains the upstream teaching system; the added utilities and their test fixtures are identified in `xv6/PROVENANCE.md` rather than presenting the entire kernel as newly authored code.
