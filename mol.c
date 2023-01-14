#include "mol.h"

void atomset (atom *atom, char element[3], double *x, double *y, double *z){
    atom->x = &x;
    atom->y = &y;
    atom->z = &z;
    strcpy(atom->element, element);
}




