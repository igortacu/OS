FROM ubuntu:24.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gcc make strace gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu \
    qemu-system-misc python3 perl procps bc && rm -rf /var/lib/apt/lists/*
WORKDIR /work
