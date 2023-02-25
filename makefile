CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all:  myprog

clean:  
	rm -f *.o *.so myprog

libmol.so: mol.o
	$(CC) mol.o -shared -o $@

mol.o:  mol.c mol.h
	$(CC) $(CFLAGS) -c $< -fPIC -o $@ 

testPart1.o:  testPart1.c mol.h
	$(CC) $(FLAGS) -c $< -o $@

myprog:  testPart1.o libmol.so
	$(CC) $< -L. -lmol -lm -o $@
	./myprog
