CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O0 -pthread
.PHONY: all clean
all: fire fire4
fire: fire.c
	$(CC) $(CFLAGS) -o $@ $<
fire4: fire.c
	$(CC) $(CFLAGS) -DTHREADS=4 -o $@ $<
clean:
	rm -f fire fire4
