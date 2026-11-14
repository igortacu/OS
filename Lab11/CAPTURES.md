# Lab 11 — Native Terminal captures

The sources and executables are prepared in `/root/os-lab11` on the Ubuntu server. Run these blocks in its SSH terminal, one block at a time. Capture the commands and their actual results. `clear` is available in Linux. Send the images so they can be embedded in the report with captions; the text logs are already saved separately.

## 1. Build and see the race

```bash
cd /root/os-lab11
clear
pwd
make clean all
for i in 1 2 3; do ./race; done
```

## 2. Correct locks and the two-permit variant

```bash
clear
for i in 1 2 3; do ./mutex; done
for i in 1 2 3; do ./sem; done
mkdir -p variants
sed 's/sem_init(&s, 0, 1)/sem_init(\&s, 0, 2)/' sem.c > variants/sem2.c
gcc -std=c11 -Wall -Wextra -O0 -pthread -o variants/sem2 variants/sem2.c
for i in 1 2 3; do ./variants/sem2; done
```

## 3. Timings

```bash
clear
time ./race
time ./mutex
time ./sem
```

## 4. Message ordering, correct and incorrect

```bash
clear
grep -n 'sem_init' order.c
./order
sed 's/sem_init(&ready, 0, 0)/sem_init(\&ready, 0, 1)/' order.c > variants/order1.c
gcc -std=c11 -Wall -Wextra -O0 -pthread -o variants/order1 variants/order1.c
./variants/order1
```

## 5. Parking, three places

```bash
clear
grep -nE 'PLACES|sem_wait|sem_post|pthread_mutex' parking.c
./parking
```

## 6. Parking, one place

```bash
clear
sed 's/#define PLACES 3/#define PLACES 1/' parking.c > variants/parking1.c
gcc -std=c11 -Wall -Wextra -O0 -pthread -o variants/parking1 variants/parking1.c
./variants/parking1
```

The race values, car order and timings may differ from the saved run. A race can occasionally print the expected count; that does not prove correctness. Keep the genuine output and discuss the difference instead of altering it.
