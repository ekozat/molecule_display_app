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
//what kind of copy?
molecule *molcopy (molecule *src){
    //wait so do we use molmalloc to create a new molecule?
    


}
// not tested
// set pointers to NULL afterward
void molfree (molecule *ptr){
    free(ptr->atom_ptrs);
    free(ptr->atoms);
    free(ptr->bond_ptrs);
    free(ptr->bonds);
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
        molecule->atoms = malloc(sizeof(struct atom)* molecule->atom_max);
        molecule->atom_ptrs = malloc(sizeof(struct atom*) * molecule->atom_max);
    }

    // have to test the realloc 
    // reallocs, then adds the atom in the next if
    if (molecule->atom_no == molecule->atom_max){
        // doubles the max
        molecule->atom_max *= 2;

        // reallocs for more memory
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom)* molecule->atom_max);
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);
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
void molappend_bond (molecule *molecule, bond *bond){

}



