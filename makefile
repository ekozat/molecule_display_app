CC = clang
CFLAGS = -std=c99 -Wall -pedantic

all: test

test: test1.o mol.o
	$(CC) $^ -o test

test1.o: test1.c mol.h
	$(CC) $(CFLAGS) -c $<

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f *.o test