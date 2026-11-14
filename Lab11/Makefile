CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O0 -pthread
PROGRAMS = race mutex sem order parking

.PHONY: all clean
all: $(PROGRAMS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS)
