CC ?= cc
CFLAGS = -std=c99 -Wall -Wextra -I../../include

SRCS = main.c ../../src/newbee_model.c

hello_skill: $(SRCS)
	$(CC) $(CFLAGS) -o $@ $(SRCS)

clean:
	rm -f hello_skill

.PHONY: clean
