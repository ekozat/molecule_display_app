#include "mol.h"
//NOTE: remove exec from Makefile when finished

/*
Questions
1) malcopy - would we use malmalloc to create a new molecule to copy into
2) makefile - would we need to put just a main.c file as a target or could we leave in test.c
    - ?
3) molappend - would we malloc when atom_max or bond_max is equal to 0 or realloc?
4) Reliable way to test if in memory?
5) Qsort - use the built in c function? Allowed separate functions from assigned (cmpfunc)
*/


// finished
// Purpose: Function should copy the values pointed to by element, x, y, and z into atom
void atomset (atom *atom, char element[3], double *x, double *y, double *z){
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    strcpy(atom->element, element);
}

//finished
// Purpose: Function should copy the values in atom to locations pointed to by element, x, y, and z
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

// Purpose: Function should copy the values a1, a2, and epairs into corresponding attributes in bond
void bondset (bond *bond, atom *a1, atom *a2, unsigned char epairs){
    bond->a1 = a1;
    bond->a2 = a2;
    bond->epairs = epairs;
}
// finished
// Purpose: Function should copy the values in bond to a1, a2, and epairs
void bondget (bond *bond, atom **a1, atom **a2, unsigned char *epairs){
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
}

// need to test
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
// use molappend to copy the pointers to the new molecule (molmalloc)
molecule *molcopy (molecule *src){
    //wait so do we use molmalloc to create a new molecule?
    


}
// not tested
// set pointers to NULL afterward
void molfree (molecule *ptr){
    free(ptr->atom_ptrs);
    ptr->atom_ptrs = NULL;

    free(ptr->atoms);
    ptr->atoms = NULL;

    free(ptr->bond_ptrs);
    ptr->bond_ptrs = NULL;

    free(ptr->bonds);
    ptr->bonds = NULL;

    free(ptr);
}
// I don't know how to test this
// It might be going into bad memory if the sort rearranges stuff
void molappend_atom (molecule *molecule, atom *atom){
    if (molecule->atom_max == 0){
        molecule->atom_max++;
        // should we malloc or no? im assuming we do
        // wait but what if we can molappend_atom and then molmalloc - realloc?
        // ^no, cause we can't call molmalloc with the same molecule

        // Check pointer address - malloc will come back as NULL if it errors
        molecule->atoms = malloc(sizeof(struct atom)* molecule->atom_max);
        molecule->atom_ptrs = malloc(sizeof(struct atom*) * molecule->atom_max);
    }

    // have to test the realloc 
    // reallocs, then adds the atom in the next if
    if (molecule->atom_no == molecule->atom_max){
        // doubles the max
        molecule->atom_max *= 2;

        // reallocs for more memory
        // atom_ptrs are pointing at the atoms memory
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom)* molecule->atom_max);
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);

        // NOTE: Do we ever have to worry about reallocing to a smaller number? probably not therefore the
        // addresses won't change for atoms
    }

    if (molecule->atom_no < molecule->atom_max){
        // put values from passed in atom into the atom stored in molecule
        // check if its actual empty space as well
        atomget(atom, molecule->atoms[molecule->atom_no].element, 
                &(molecule->atoms[molecule->atom_no].x),
                &(molecule->atoms[molecule->atom_no].y),
                &(molecule->atoms[molecule->atom_no].z));

        printf("%f\n", molecule->atoms[molecule->atom_no].x);
        printf("%s\n", molecule->atoms[molecule->atom_no].element);
        // printf("%f\n", molecule->atoms[1000].x);

        molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
        
        molecule->atom_no++;
    }
}
// is it any different for bonds?
// more complicated because of the atom pointers
void molappend_bond (molecule *molecule, bond *bond){
    // would we malloc two atoms? Good test case: checking if the amount of atoms makes sense 
    // for the amount of bonds
     if (molecule->bond_max == 0){
        molecule->bond_max++;

        // Check pointer address - malloc will come back as NULL if it errors
        molecule->bonds = malloc(sizeof(struct bond)* molecule->bond_max);
        molecule->bond_ptrs = malloc(sizeof(struct bond*) * molecule->bond_max);
    }
    
    // have to test the realloc 
    // reallocs, then adds the atom in the next if
    if (molecule->bond_no == molecule->bond_max){
        // doubles the max
        molecule->bond_max *= 2;

        // reallocs for more memory
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond)* molecule->bond_max);
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);
    }

     if (molecule->bond_no < molecule->bond_max){
        bondget(bond, &molecule->bonds[molecule->bond_no].a1, 
                &molecule->bonds[molecule->bond_no].a2, 
                &molecule->bonds[molecule->bond_no].epairs);
        
        
        printf("bond1: a1 - %p, a2 - %p\n",  molecule->bonds->a1, molecule->bonds->a2);

        printf("%f\n", molecule->bonds->a1[0].x);
        printf("%s\n", molecule->bonds->a1[0].element);
        // printf("%f\n", molecule->atoms[1000].x);

        molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
        
        molecule->bond_no++;
    }
}

void mol_sort (molecule *molecule){

}

int cmpfunc (const void *a, const void *b){
    double *double_ptr_l, *double_ptr_r;

    // Get the values at given addresses
    double_ptr_l = (double *)a;
    double_ptr_r = (double *)b;

    // return the smaller of the two (must be an int - qsort will fail with a double)
    // doesn't matter that it's truncation
    return (int)(*double_ptr_l - *double_ptr_r);
}



