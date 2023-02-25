CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all:  myprog

clean:  
	rm -f *.o *.so myprog

mol.o:  mol.c mol.h
	$(CC) $(CFLAGS) -c $< -fPIC -o $@ 

libmol.so: mol.o
	$(CC) $< -shared -o $@

molecule_wrap.c molecule.py: molecule.i
	swig3.0 -python -outdir . -o molecule_wrap.c -module molecule molecule.i

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c $< -fPIC -I/usr/include/python3.7m -o $@
 
_molecule.so: molecule_wrap.o
	$(CC) -shared -o $@ -dynamiclib -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -lpython3.7m -L. -lmol $<

testPart1.o:  testPart1.c mol.h
	$(CC) $(FLAGS) -c $< -o $@

myprog:  testPart1.o libmol.so _molecule.so
	$(CC) $< -L. -lmol -lm -o $@
	./myprog
