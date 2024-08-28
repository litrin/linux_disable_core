CC=cc
AR=
CFLAGS=-O3

ALL:
	$(CC) $(CFLAGS) core_enable.c  -o core_enable


install:
	cp core_enable /usr/local/bin/core_enable

clean:
	rm -rf core_enable
