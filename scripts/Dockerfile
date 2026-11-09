FROM ubuntu:24.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gcc make strace gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu \
    qemu-system-misc python3 perl procps bc util-linux file man-db manpages && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --uid 1001 --shell /bin/bash labstudent
WORKDIR /work
