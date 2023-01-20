#include "mol.h"

//fully finished function
void atomset (atom *atom, char element[3], double *x, double *y, double *z){
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    strcpy(atom->element, element);
}

//somethings wrong
void atomget (atom *atom, char element[3], double *x, double *y, double *z){
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
    strcpy(element, atom->element);
}

void bondset (bond *bond, atom *a1, atom *a2, unsigned char epairs){
    bond->a1 = &(atom->a1);
    bond->a2 = &(atom->a2);
    bond->epairs = epairs;
}
void bondget (bond *bond, atom **a1, atom **a2, unsigned char *epairs){

}
molecule *molmalloc (unsigned short atom_max, unsigned short bond_max){

}
molecule *molcopy (molecule *src){

}
void molfree (molecule *ptr){

}
void molappend_atom (molecule *molecule, atom *atom){

}
void molappend_bond (molecule *molecule, bond *bond){

}



