# Applying the Lab 10 patch

`trace.patch` is a Git-generated diff for MIT xv6-riscv revision
`e93dabeb98431235c6e1a101cb96c73c923fdbc4`. That revision has sync=22;
this patch assigns trace=23. Check out the exact base before applying it:

```sh
git clone https://github.com/mit-pdos/xv6-riscv.git /tmp/xv6-trace-check
cd /tmp/xv6-trace-check
git checkout e93dabeb98431235c6e1a101cb96c73c923fdbc4
git apply --check /absolute/path/to/trace.patch
git apply /absolute/path/to/trace.patch
make -j2 kernel/kernel fs.img
make qemu CPUS=1
```

Alternatively run `python3 scripts/check-trace-patch.py /tmp/xv6-trace-check
/absolute/path/to/trace.patch` from the OS repository **before** applying the
patch. The checker requires a clean disposable checkout at the exact base.
It applies the patch, temporarily removes the syscall dispatch registration
for the intentional Check 1 control, restores it, and rebuilds and tests the
final implementation. The source is restored even if the control test fails.

The raw record is [trace-patch-validation.txt](evidence/trace-patch-validation.txt).
It contains the patch checks, compilation, `unknown sys call 23` control,
final mask tests, and passing fork inheritance test. This is an additional
verification run, separate from the main lab execution transcript.

The complete buildable implementation is also available under `../xv6`.
