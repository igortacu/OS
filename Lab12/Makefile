CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O0 -pthread
PROGRAMS = prodcons condvar readers deadlock

.PHONY: all clean variants
all: $(PROGRAMS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

variants:
	python3 prepare-variants.py
	$(CC) $(CFLAGS) -o variants/prodcons_bad variants/prodcons_bad.c
	$(CC) $(CFLAGS) -o variants/condvar_if variants/condvar_if.c
	$(CC) $(CFLAGS) -o variants/deadlock_bad variants/deadlock_bad.c
	$(CC) $(CFLAGS) -o variants/deadlock_nosleep variants/deadlock_nosleep.c

clean:
	rm -f $(PROGRAMS)
