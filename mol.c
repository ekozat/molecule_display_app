#include "mol.h"
#include <math.h>
//NOTE: remove exec from Makefile when finished

/*
Questions
2) makefile - would we need to put just a main.c file as a target or could we leave in test.c
    - ?
3) molappend - would we malloc when atom_max or bond_max is equal to 0 or realloc?
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
    
    if (atom == NULL){
        return;
    }

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
// double pointers because passed by reference
void bondget (bond *bond, atom **a1, atom **a2, unsigned char *epairs){
    
    if (bond == NULL){
        return;
    }

    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
}

// need to test
molecule *molmalloc (unsigned short atom_max, unsigned short bond_max){
    //assign memory for molecule struct
    molecule *mol = malloc(sizeof(struct molecule));
    if (mol == NULL){
        return NULL;
    }

    //atom array (holding all atom values)
    mol->atoms = malloc(sizeof(struct atom)* atom_max);
    if (mol->atoms == NULL){
        return NULL;
    }
    //atom pointer array (pointing to atom pointer to each element from the bond array)
    mol->atom_ptrs = malloc(sizeof(struct atom*) * atom_max);
    if (mol->atom_ptrs == NULL){
        return NULL;
    }

    mol->bonds = malloc(sizeof(struct bond) * bond_max);
    if (mol->bonds == NULL){
        return NULL;
    }

    mol->bond_ptrs = malloc(sizeof(struct bond*) * bond_max);
    if (mol->bond_ptrs == NULL){
        return NULL;
    }

    mol->atom_max = atom_max;
    mol->atom_no = 0;
    mol->bond_max = bond_max;
    mol->bond_no = 0;
    
    return mol;
}

// need to test 
// bond copied atom pointers will point to the original molecules 
molecule *molcopy (molecule *src){

    if (src == NULL){
        return NULL;
    }

    // mallocs new molecule
    molecule *mol_new = molmalloc(src->atom_max, src->bond_max);

    // since molmalloc auto assigns atom_no to 0, we change that
    // mol_new->atom_no = src->atom_no;
    // mol_new->bond_no = src->bond_no;

    // use molappend to add the existing atoms and bonds onto the new mol
    for (int i = 0; i < src->atom_no; i++){
        molappend_atom(mol_new, &src->atoms[i]);   
    }

    for (int i = 0; i < src->bond_no; i++){
        molappend_bond(mol_new, &src->bonds[i]);
    }

    return mol_new;
}

// valgrind works!
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

    if (molecule == NULL || atom == NULL){
        return;
    }

    if (molecule->atom_max == 0){
        molecule->atom_max++;
        // should we malloc or no? im assuming we do
        // wait but what if we can molappend_atom and then molmalloc - realloc?
        // ^no, cause we can't call molmalloc with the same molecule

        // Check pointer address - malloc will come back as NULL if it errors
        molecule->atoms = malloc(sizeof(struct atom)* molecule->atom_max);
        if (molecule->atoms == NULL){
            return;
        }

        molecule->atom_ptrs = malloc(sizeof(struct atom*) * molecule->atom_max);
        if (molecule->atom_ptrs == NULL){
            return;
        }
    }

    // have to test the realloc 
    // reallocs, then adds the atom in the next if
    if (molecule->atom_no == molecule->atom_max){
        // doubles the max
        molecule->atom_max *= 2;

        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom)* molecule->atom_max);
        if (molecule->atoms == NULL){
            return;
        }

        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);
        if (molecule->atom_ptrs == NULL){
            return;
        }

        // if realloc - make sure atom_ptrs point to the new memory locations
        // append after sorting might be an issue
        for (int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }

    if (molecule->atom_no < molecule->atom_max){
        // put values from passed in atom into the atom stored in molecule
        // check if its actual empty space as well
        atomget(atom, molecule->atoms[molecule->atom_no].element, 
                &(molecule->atoms[molecule->atom_no].x),
                &(molecule->atoms[molecule->atom_no].y),
                &(molecule->atoms[molecule->atom_no].z));

        // printf("%f\n", molecule->atoms[molecule->atom_no].x);
        // printf("%s\n", molecule->atoms[molecule->atom_no].element);
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
    if (molecule == NULL || bond == NULL){
        return;
    }


    if (molecule->bond_max == 0){
        molecule->bond_max++;

        // Check pointer address - malloc will come back as NULL if it errors
        molecule->bonds = malloc(sizeof(struct bond)* molecule->bond_max);
        if (molecule->bonds == NULL){
            return;
        }

        molecule->bond_ptrs = malloc(sizeof(struct bond*) * molecule->bond_max);
        if (molecule->bond_ptrs == NULL){
            return;
        }
    }
    
    // have to test the realloc 
    // reallocs, then adds the atom in the next if
    if (molecule->bond_no == molecule->bond_max){
        // doubles the max
        molecule->bond_max *= 2;

        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond)* molecule->bond_max);
        if (molecule->bonds == NULL){
            return;
        }

        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);
        if (molecule->bond_ptrs == NULL){
            return;
        }

        for (int i = 0; i < molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }

     if (molecule->bond_no < molecule->bond_max){
        bondget(bond, &molecule->bonds[molecule->bond_no].a1, 
                &molecule->bonds[molecule->bond_no].a2, 
                &molecule->bonds[molecule->bond_no].epairs);

        //test functions
        // printf("%f\n", molecule->bonds[molecule->bond_no].a1[0].x);
        // printf("%s\n", molecule->bonds[molecule->bond_no].a1[0].element);
        // printf("%c\n", molecule->bonds[molecule->bond_no].epairs);

        molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
        
        molecule->bond_no++;
    }
}

// should sort atom_ptrs in order of increasing z value
// also bond_ptrs = take the avg
void molsort (molecule *molecule)
{
    if (molecule == NULL){
        return;
    }

    // sorted atom_ptrs array
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), cmpfunc_atom);

    //sort the bonds
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), cmpfunc_bond);
}

void xrotation (xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0);
    double cos_val = cos(rad);
    double sin_val = sin(rad);

    xform_matrix[0][0] = 1; xform_matrix[0][1] = 0; xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0; xform_matrix[1][1] = cos_val; xform_matrix[1][2] = -sin_val;
    xform_matrix[2][0] = 0; xform_matrix[2][1] = sin_val; xform_matrix[2][2] = cos_val;

    // printf("%f\n", sin_val);
}

void yrotation (xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0);
    double cos_val = cos(rad);
    double sin_val = sin(rad);

    xform_matrix[0][0] = cos_val; xform_matrix[0][1] = 0; xform_matrix[0][2] = sin_val;
    xform_matrix[1][0] = 0; xform_matrix[1][1] = 1; xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin_val; xform_matrix[2][1] = 0; xform_matrix[2][2] = cos_val;
}

void zrotation (xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0);
    double cos_val = cos(rad);
    double sin_val = sin(rad);

    xform_matrix[0][0] = cos_val; xform_matrix[0][1] = -sin_val; xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin_val; xform_matrix[1][1] = cos_val; xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0; xform_matrix[2][1] = 0; xform_matrix[2][2] = 1;
}

void mol_xform (molecule *molecule, xform_matrix matrix){

    if (molecule == NULL){
        return;
    }

    double x_vector, y_vector, z_vector;

    for (int i = 0; i < molecule->atom_no; i++){
        x_vector = molecule->atoms[i].x;
        y_vector = molecule->atoms[i].y;
        z_vector = molecule->atoms[i].z;

        // printf("%f ", molecule->atoms[i].x);
        // printf("%f ", matrix[2][0]);
        // printf("%f ,", molecule->atoms[i].x * matrix[2][0]);

        // printf("%f ", molecule->atoms[i].y);
        // printf("%f ", matrix[2][1]);
        // printf("%f ,", molecule->atoms[i].y * matrix[2][1]);

        // printf("%f ", molecule->atoms[i].z);
        // printf("%f ", matrix[2][2]);
        // printf("%f ,", molecule->atoms[i].z * matrix[2][2]);

        molecule->atoms[i].x = matrix[0][0] * x_vector + matrix[0][1] * y_vector + matrix[0][2] * z_vector;
        molecule->atoms[i].y = matrix[1][0] * x_vector + matrix[1][1] * y_vector + matrix[1][2] * z_vector;
        molecule->atoms[i].z = matrix[2][0] * x_vector + matrix[2][1] * y_vector + matrix[2][2] * z_vector;

        // printf("%f ", matrix[2][0] * molecule->atoms[i].x + matrix[2][1] * molecule->atoms[i].y + matrix[2][2] * molecule->atoms[i].z);
        // printf("%f\n",  molecule->atoms[i].z);

    }
}

// works with test2!
int cmpfunc_atom (const void *a, const void *b){
    // we are sorting atom ptrs
    struct atom *a_atom, *b_atom;

    // We passed in two double pointers because they point to the address of the
    // the elements in the array, which is a struct atom pointer. We dereference
    // to get the individual element as a pointer.
    a_atom = *(struct atom **)a;
    b_atom = *(struct atom **)b;

    // test functions
    // printf("%f %f\n", a_atom->z, b_atom->z);
    // printf("%d\n",  (int)(a_atom->z - b_atom->z));

    // doesn't matter if it truncates
    return (int)(a_atom->z - b_atom->z);
}

// works with test2! 
int cmpfunc_bond (const void *a, const void *b){
    struct bond *a_bond, *b_bond;

    a_bond = *(struct bond **)a;
    b_bond = *(struct bond **)b;

    double a_avg = (a_bond->a1->z + a_bond->a2->z) / 2;
    double b_avg = (b_bond->a1->z + b_bond->a2->z) / 2;

    return (int)(a_avg - b_avg);
}


