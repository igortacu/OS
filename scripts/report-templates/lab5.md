# Lab 5 Files names permissions and storage on Linux

Tacu Igor, FAF 242\
Operating Systems, Technical University of Moldova\
Run on 9 November 2026

## Purpose and required execution identity

The experiment connects pathnames, inodes, permissions and disk allocation using the original Lab 5 commands. Every command here ran on the Ubuntu x86_64 server as `oslab_igor`, UID 1001, without sudo or extra groups. An ordinary user's failures demonstrate permission checks that root may bypass. The complete recording is `Lab5-6/evidence/linux.txt`; the command sequence is `scripts/run-lab5.sh`.

```text
@@L5_ID@@
```

## Part 1 The tree and file types

The first letters in ls identified `/etc` and `/tmp` as directories (`d`), `/etc/passwd` as a regular file (`-`), `/bin` as a symbolic link (`l`), and `/dev/null` as a character device (`c`). `/bin` resolves to `/usr/bin`. File recognized ls as an ELF executable and passwd as text. A character device was `/dev/zfs`; a block device was `/dev/sr0`.

The accessible recursive totals were 476 MiB for `/var/log` and 3.5 GiB for `/usr`, making usr approximately seven to eight times larger. As requested, the du commands suppress permission diagnostics; inaccessible entries can make an ordinary user's total incomplete. These values describe this server at the time of the run.

```text
@@L5_TYPES@@
```

## Part 2 Inodes links and allocation

Stat showed inode 3113 and Links 1 for notes.txt. The inode number identifies the object; Links counts directory names referring to it. After ln, notes.txt and hard.txt both reported inode 3113 and two links. Removing notes.txt deleted one directory entry, leaving the data accessible through hard.txt with one link.

Soft.txt had a separate inode and an eight-byte length, exactly the length of its stored relative target `hard.txt`. After that target was deleted, soft.txt still existed but cat failed to resolve it. A symlink stores a pathname, not an additional hard link to the target inode.

```text
@@L5_LINKS@@
```

A new directory had two links: its entry in the parent and its own dot entry. The dot-dot entries in two new child directories added two references, making the parent's link count four. The two-byte one.txt consumed a 4 KiB allocation unit. Sparse big.img had logical length 1 GiB but no allocated data blocks, so du returned zero. File length and storage consumption measure different things.

## Part 3 Permissions

The requested modes are 600 = `rw-------` for a private file; 644 = `rw-r--r--` for an ordinary shared-readable document; 755 = `rwxr-xr-x` for a public executable or traversable directory; and 700 = `rwx------` for a private executable or directory. Ownership selects the owner permission class; it does not override zero owner-read bits. Cat therefore failed at mode 000 even though the user owned s.txt. Restoring owner-read permission made the file readable.

Umask was 0022. Default file mode 0666 masked by 0022 became 0644, while default directory mode 0777 became 0755. This is bit masking: the mask removes requested permissions and cannot add execute bits to an ordinary new file.

```text
@@L5_PERMS@@
```

With only read permission on box, ls could read the name f but cat could not traverse the directory to open box/f. With only execute permission, ls could not list names but cat could access the already-known pathname. Directory r permits reading entries, while x permits searching and traversing them. These outcomes were actually observed under the unprivileged identity.

The s on `/usr/bin/passwd` is set-user-ID: its controlled code can execute with the file owner's effective identity to update protected password information. The t on `/tmp` is the sticky bit, restricting removal of other users' entries in a shared writable directory. Reading `/etc/shadow` was denied to oslab_igor, consistent with root/shadow ownership and its restricted mode. No password hashes were recorded.

## Part 4 Disk diagram and proc

The disk diagram below shows sda, approximately 38.1 GiB, with sda1 as the ext4 root filesystem, sda14 as a 1 MiB boot-related partition without a displayed mount, and sda15 as a 256 MiB vfat EFI filesystem mounted at `/boot/efi`. Sr0 is a separate optical device. Root usage was 38 GiB total, 14 GiB used, 22 GiB available and 39 percent use; rounding and filesystem reservations explain why displayed columns need not sum exactly.

```text
@@L5_DISK@@
```

Proc reported two processor entries and MemTotal 3,911,572 KiB, approximately 3.73 GiB. MemAvailable is an observation of the current workload, not installed capacity. Reading `/proc/self/status` with head reported Name head because self resolves for the process reading it. Likewise the fd listing described ls's own descriptors, including its open directory descriptor 3. Descriptors 1 and 2 point to the saved recording in this run because output was redirected there.

## Conclusion

The outputs distinguish names from inode identity, symlink contents from target existence, and logical length from allocated space. The non-root identity makes the permission failures meaningful. Disk and proc values are observations of the actual Ubuntu server. Optional stretch exercises are not claimed as completed.

## Execution captures and code excerpts

The native Terminal screenshot below was supplied by the author from a direct unprivileged permission test. The earlier full raw execution recording remains in the repository. This additional live check uses a separate temporary directory.

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth,height=0.81\textheight,keepaspectratio]{Lab5-6/evidence/screenshots/lab5-permissions-terminal.png}
\caption{Unprivileged permission checks}
\end{figure}
