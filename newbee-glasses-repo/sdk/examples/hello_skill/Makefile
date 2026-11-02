CC ?= cc
CFLAGS = -std=c99 -Wall -Wextra -I../../include

hello_skill: main.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f hello_skill

.PHONY: clean
