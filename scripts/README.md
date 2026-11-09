# Reproduce the November 9 experiments

The submitted evidence was collected on Ubuntu 24.04 ARM64 in Docker, with QEMU executing the integrated RISC-V source. These are new runs on the author's machine, distinct from the older remote-server observations. The PDF console blocks are formatted excerpts; raw output is committed without removing the prompt control sequences from the interactive PTY test.

From the repository root, build the Linux tooling image and run the experiments:

```sh
docker build -t os-lab-reproduction -f scripts/Dockerfile .
docker run --rm -v "$PWD:/work" os-lab-reproduction bash scripts/run-linux.sh
docker run --rm -v "$PWD:/work" os-lab-reproduction python3 scripts/check-interactive-bash.py
docker run --rm -v "$PWD:/work" os-lab-reproduction python3 scripts/run-xv6.py
```

The xv6 runner recreates only the generated `xv6/fs.img` test disk. Do not use it with a generated disk containing files you want to keep. It compiles the kernel and user programs, boots one hart, and verifies distinctive output in Labs 4, 6, 8, and 10. The Linux runner uses temporary directories so it does not alter the user's own lab files.

For PDFs, install Pandoc, XeLaTeX, the Arial font, and Poppler's `pdfseparate` and `pdfunite`. Then run `python3 scripts/build-reports.py` on the host. Authored report templates are under `scripts/report-templates`, while the generated Markdown is stored with each report. The Linux Lab 5 pages are preserved when replacing the xv6 Lab 6 section of the joint PDF.

The lab log is generated test data, not real traffic. The programs were implemented or revised with coding assistance, and the tests are automated. The source provenance file identifies MIT xv6 as upstream. No originality percentage is asserted; this revision provides new executions, source availability, and explanations that can be checked against those executions.
