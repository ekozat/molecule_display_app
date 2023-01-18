CC = gcc
CFLAGS = -std=c99 -Wall -pedantic

all: main

main: main.o mol.o
	$(CC) $(CFLAGS) main.o mol.o -o main

main.o: main.c
	$(CC) $(CFLAGS) main.c 

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) mol.c

clean:
	rm -f *.o main