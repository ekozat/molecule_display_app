#include "mol.h"
//NOTE: remove exec from Makefile when finished


//fully finished function
void atomset (atom *atom, char element[3], double *x, double *y, double *z){
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    strcpy(atom->element, element);
}

//make sure to allocate atom memory before testing - works correctly
void atomget (atom *atom, char element[3], double *x, double *y, double *z){
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
    strcpy(element, atom->element);
}

//should it be a deep copy? - test if bond 2 changes if you make changes to bond 1
//NOTE: you are not copying atom structures, only the addresses of the atom
// structures
//Check for atom values seems to be good - bond atom pointing at the atom
void bondset (bond *bond, atom *a1, atom *a2, unsigned char epairs){
    bond->a1 = a1;
    bond->a2 = a2;
    bond->epairs = epairs;
}
// tested!
void bondget (bond *bond, atom **a1, atom **a2, unsigned char *epairs){
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
}
molecule *molmalloc (unsigned short atom_max, unsigned short bond_max){
    //assign memory for molecule struct
    molecule *mol = malloc(sizeof(struct molecule));

    //atom array (holding all atom values)
    mol->atoms = malloc(sizeof(struct atom)* atom_max);
    //atom pointer array (pointing to atom pointer to each element from the bond array)
    mol->atom_ptrs = malloc(sizeof(struct atom*) * atom_max);

    mol->bonds = malloc(sizeof(struct bond) * bond_max);
    mol->bond_ptrs = malloc(sizeof(struct bond*) * bond_max);

    mol->atom_max = atom_max;
    mol->atom_no = 0;
    mol->bond_max = bond_max;
    mol->bond_no = 0;
    
    return mol;
}
molecule *molcopy (molecule *src){

}
void molfree (molecule *ptr){

}
void molappend_atom (molecule *molecule, atom *atom){

}
void molappend_bond (molecule *molecule, bond *bond){

}



