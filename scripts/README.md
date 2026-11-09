# Reproduce the November 9 experiments

The submitted evidence was collected on Ubuntu 24.04 x86_64 over SSH on 9 November 2026. QEMU executes the integrated RISC-V source in an isolated copy. Lab 5 runs as the unprivileged oslab_igor account. Report figures now use author-supplied native Terminal screenshots of direct execution and source inspection. Two labeled patch-audit figures show saved verification output. Earlier raw logs and browser-view assets are retained as provenance, and full source files are included.

The Docker image below provides an alternative reproduction environment. Disk names, inode numbers, PIDs, timing, and locale-dependent syscall counts may differ. For the original handout cases also run `python3 scripts/check-lab3-spec.py`, `python3 scripts/check-broken-pipeline.py`, and, as a non-root user, `bash scripts/run-lab5.sh`.

From the repository root, build the Linux tooling image and run the experiments:

```sh
docker build -t os-lab-reproduction -f scripts/Dockerfile .
docker run --rm -v "$PWD:/work" os-lab-reproduction bash scripts/run-linux.sh
docker run --rm -v "$PWD:/work" os-lab-reproduction python3 scripts/check-interactive-bash.py
docker run --rm -v "$PWD:/work" os-lab-reproduction python3 scripts/run-xv6.py
```

The xv6 runner recreates only the generated `xv6/fs.img` test disk. Do not use it with a generated disk containing files you want to keep. It compiles the kernel and user programs, boots one hart, and verifies distinctive output in Labs 4, 6, 8, and 10. The Linux runner uses temporary directories so it does not alter the user's own lab files.

For PDFs, install Pandoc, XeLaTeX, the Arial font, and Poppler's `pdfseparate` and `pdfunite`. Then run `python3 scripts/build-reports.py` on the host. Authored report templates are under `scripts/report-templates`, while the generated Markdown is stored with each report. Both Lab 5 and Lab 6 sections are generated from the new runs.

The lab log is generated test data, not real traffic. The programs were implemented or revised with coding assistance, and the tests are automated. The source provenance file identifies MIT xv6 as upstream. No originality percentage is asserted; this revision provides new executions, source availability, and explanations that can be checked against those executions.
