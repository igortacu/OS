# Operating Systems · FCIM / FAF · UTM · 2026-2027

## The OS as a Resource Manager

**Lab 1 · Track A: the real OS, from the outside (Linux) · 90 minutes**

---

## Goal

In today's lecture you met the operating system as the manager that stands between your programs and the hardware. In this lab you will see that manager at work with your own eyes, on the provided Linux virtual machine. You will watch the four core jobs of any OS (managing files, processes, memory and devices) happen live in the terminal, and you will write down what you observe (not just which command you typed).

## Before you start

- Log in to the provided Linux VM and open a terminal.
- You do not need to install anything. Everything used here is already present.
- Create a working folder and keep a file called `report.md` open beside the terminal.

```bash
mkdir -p ~/os-lab1 && cd ~/os-lab1
whoami          # who am I to the OS
uname -a        # which kernel is managing this machine
uptime          # how long has this OS been running
```

> **How you hand this in**
>
> Throughout the lab, copy interesting output and short answers into `report.md`. You submit that single file at the end via git (your assistant will pull it). Nothing goes by e-mail.

---

## Part 1. Files and directories (File management, ~20 min)

The OS turns a raw disk into a tidy tree of named files with owners and permissions. Explore that tree and change it.

1. Navigate and inspect:

```bash
pwd                  # where am I
ls -la /             # the root of the whole tree
ls -la ~             # my home directory
cd /etc && ls | head
```

2. Create, copy, rename, remove, and watch the tree change:

```bash
cd ~/os-lab1
mkdir demo && cd demo
echo "hello operating systems" > note.txt
cp note.txt copy.txt
mv copy.txt renamed.txt
ls -l
rm renamed.txt
```

3. Look at ownership and permissions. The OS decides who may touch what:

```bash
ls -l note.txt      # read the rwx / owner / group columns
chmod 600 note.txt  # owner-only read+write
ls -l note.txt
chmod 644 note.txt
```

> **Observe (write in report.md)**
>
> 1. Who owns the files you just created, and which group?
> 2. What do the ten characters at the start of `ls -l` mean for `note.txt` after `chmod 600`?
> 3. Name two directories directly under `/` and say, in one line each, what they hold.

---

## Part 2. Processes (Process management, ~20 min)

Every running program is a process the OS created, isolated and schedules. Find them, start one, and stop it.

4. List the processes the OS is currently juggling:

```bash
ps aux | head
ps aux | wc -l   # how many processes exist right now
top              # live view; press q to quit
```

5. Start a background process, find it, then stop it:

```bash
sleep 300 &              # run in the background; note the PID printed
jobs                     # shell view of background jobs
ps -ef | grep sleep      # find it among all processes
kill <PID>               # ask the OS to terminate it (use the PID above)
```

6. Peek at what the kernel exposes about a process through the `/proc` pseudo-filesystem:

```bash
sleep 300 &
PID=$!
ls /proc/$PID/
cat /proc/$PID/status | head -20   # state, memory, threads
kill $PID
```

> **Observe (write in report.md)**
>
> 1. What is the PID of process number 1, and what is it (look it up)?
> 2. Roughly how many processes were running on your idle VM?
> 3. From `/proc/<pid>/status`, what does the "State:" line say for your sleeping process?

---

## Part 3. Memory (Memory management, ~15 min)

The OS hands each process its own view of memory and shares the physical RAM between them. Look at the totals and at one process.

```bash
free -h                        # total / used / free RAM and swap
cat /proc/meminfo | head -6
sleep 300 & PID=$!
grep VmRSS /proc/$PID/status   # real RAM used by this process
kill $PID
```

> **Observe (write in report.md)**
>
> 1. How much total RAM does the VM have, and how much is free?
> 2. What is swap, and how much is configured?
> 3. How much resident memory (VmRSS) does a bare `sleep` process use, and does that surprise you?

---

## Part 4. Devices and storage (I/O management, ~15 min)

The OS hides every disk, terminal and device behind uniform file-like interfaces. That is the "everything is a file" idea of UNIX.

```bash
df -h                  # mounted filesystems and free space
lsblk                  # the block devices (disks) themselves
du -sh ~/os-lab1       # size of your work folder
ls -l /dev | head      # devices presented as files
mount | head
```

> **Observe (write in report.md)**
>
> 1. Which device is your root filesystem "/" mounted on?
> 2. Give one entry from `/dev` and say what real thing it stands for.
> 3. In one sentence: what does "everything is a file" mean, based on what you saw?

---

## Wrap-up and deliverable (~15 min)

Finish `report.md` so that it contains, for each of the four parts, the answers to the "Observe" boxes plus one command output you found interesting. Close with three sentences: name the four resources the OS manages and, for each, one command that let you see it.

**You submit:**

- `report.md`: your observations and answers (the only required file).

Push it to your course repository; the assistant will pull it. Nothing by e-mail.

## Grading (out of 10)

| Criterion | Points |
|---|---|
| All four parts attempted, commands actually run | 4 |
| "Observe" questions answered correctly and in your own words | 4 |
| Closing synthesis (four resources + one command each) | 2 |

## Finished early? (optional, not graded)

If `htop` is installed, try it instead of `top`. Then run `strace -c ls` and look at the list of system calls: these are the requests your program made to the OS just to list a directory.
