#!/usr/bin/env bash
# Run on Linux. Variants are separate files; the five submitted sources stay intact.
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p evidence variants
exec > >(tee evidence/execution.txt) 2>&1
set -x
date -u '+%Y-%m-%d %H:%M:%S UTC'
uname -srmo
gcc --version | head -n 1
make clean all
for i in 1 2 3; do ./race; done
for i in 1 2 3; do ./mutex; done
for i in 1 2 3; do ./sem; done
/usr/bin/time -p ./race
/usr/bin/time -p ./mutex
/usr/bin/time -p ./sem
sed 's/sem_init(&s, 0, 1)/sem_init(\&s, 0, 2)/' sem.c > variants/sem2.c
gcc -std=c11 -Wall -Wextra -O0 -pthread -o variants/sem2 variants/sem2.c
for i in 1 2 3; do ./variants/sem2; done
./order
sed 's/sem_init(&ready, 0, 0)/sem_init(\&ready, 0, 1)/' order.c > variants/order1.c
gcc -std=c11 -Wall -Wextra -O0 -pthread -o variants/order1 variants/order1.c
./variants/order1
./parking | tee evidence/parking3.txt
sed 's/#define PLACES 3/#define PLACES 1/' parking.c > variants/parking1.c
gcc -std=c11 -Wall -Wextra -O0 -pthread -o variants/parking1 variants/parking1.c
./variants/parking1 | tee evidence/parking1.txt
sha256sum race.c mutex.c sem.c order.c parking.c
