#include "mol.h"
#include <math.h>

#define M_PI 3.14159265358979323846264338

// Purpose: Function should copy the values pointed to by element, x, y, and z into atom
void atomset (atom *atom, char element[3], double *x, double *y, double *z){
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    strcpy(atom->element, element);
}

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

// Purpose: Function should copy paramater values into bond
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;

    bond->atoms = *atoms;

    compute_coords(bond);
}

// Purpose: Function should copy attributes in bond to parameters
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){

    if (bond == NULL){
        return;
    }

    *a1 = bond->a1;
    *a2 = bond->a2;

    *epairs = bond->epairs;
    *atoms = bond->atoms;
}


// Purpose: Assigning memory for the new molecule and all attributes/structs belonging to it
molecule *molmalloc (unsigned short atom_max, unsigned short bond_max){
    
    molecule *mol = malloc(sizeof(struct molecule));
    if (mol == NULL){
        return NULL;
    }

    mol->atoms = malloc(sizeof(struct atom)* atom_max);
    if (mol->atoms == NULL){
        return NULL;
    }

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

// Purpose: Copying an existing molecule into a new molecule - with existing atoms and bonds added
molecule *molcopy (molecule *src){

    if (src == NULL){
        return NULL;
    }

    // mallocs new molecule
    molecule *mol_new = molmalloc(src->atom_max, src->bond_max);

    // use molappend to add the existing atoms and bonds onto the new mol
    for (int i = 0; i < src->atom_no; i++){
        molappend_atom(mol_new, &src->atoms[i]);   
    }
    
    for (int i = 0; i < src->bond_no; i++){
        molappend_bond(mol_new, &src->bonds[i]);
    }

    return mol_new;
}

// Purpose: free all memory from the molecule
void molfree (molecule *ptr){
    free(ptr->atom_ptrs);
    ptr->atom_ptrs = NULL;

    free(ptr->atoms);
    ptr->atoms = NULL;

    free(ptr->bond_ptrs);
    ptr->bond_ptrs = NULL;

    // free bond atom pointers
    // free(ptr->bonds->a1);
    // free(ptr->bonds->a2);

    free(ptr->bonds);
    ptr->bonds = NULL;

    free(ptr);
}

// Purpose: A new atom gets appended to the array of atoms existing within the molecule
void molappend_atom (molecule *molecule, atom *atom){

    if (molecule == NULL || atom == NULL){
        return;
    }

    // if the atom_max is 0, increase to 1 and malloc space for one atom
    if (molecule->atom_max == 0){
        molecule->atom_max++;

        molecule->atoms = malloc(sizeof(struct atom)* molecule->atom_max);
        if (molecule->atoms == NULL){
            return;
        }

        molecule->atom_ptrs = malloc(sizeof(struct atom*) * molecule->atom_max);
        if (molecule->atom_ptrs == NULL){
            return;
        }
    }

    // if there is no space to add a new atom, expand the memory of the array
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

        // assign atom_ptrs point to the new memory locations of the atoms
        for (int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }

    // add the atom
    if (molecule->atom_no < molecule->atom_max){
        
        //switch to atomset and test with A1 as well
        atomset(&molecule->atoms[molecule->atom_no], atom->element,
                &atom->x, &atom->y, &atom->z);

        // assign the atom pointers to the atoms
        molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
        
        // since we added an atom to the array, increase total atom number
        molecule->atom_no++;
    }
}

// Purpose: A new bond gets appended to the array of bonds existing within the molecule
void molappend_bond (molecule *molecule, bond *bond){

    if (molecule == NULL || bond == NULL){
        return;
    }

    // if the bond_max is 0, increase to 1 and malloc space for one bond
    if (molecule->bond_max == 0){
        molecule->bond_max++;

        molecule->bonds = malloc(sizeof(struct bond)* molecule->bond_max);
        if (molecule->bonds == NULL){
            return;
        }

        molecule->bond_ptrs = malloc(sizeof(struct bond*) * molecule->bond_max);
        if (molecule->bond_ptrs == NULL){
            return;
        }
    }
    
    // if there is no space to add a new bond, expand the memory of the array
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

    // add bond
    if (molecule->bond_no < molecule->bond_max){
        // call with the molecule atoms to get bond atoms array to point to it
        bondset(&molecule->bonds[molecule->bond_no], &bond->a1, &bond->a2,
                &molecule->atoms, &bond->epairs);

        molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
        
        molecule->bond_no++;
    }
}

// Purpose: Should sort both atom_ptrs and bond_ptrs in order of increasing z value.
// Bond_ptrs will take the average of their two atoms' z value.
void molsort (molecule *molecule)
{
    if (molecule == NULL){
        return;
    }

    // sorted atom_ptrs array
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), cmpfunc_atom);

    //sort the bond_ptrs
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), cmpfunc_bond);
}

// Purpose: Assigns the x transformation matrix
void xrotation (xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0);
    double cos_val = cos(rad);
    double sin_val = sin(rad);

    xform_matrix[0][0] = 1; xform_matrix[0][1] = 0; xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0; xform_matrix[1][1] = cos_val; xform_matrix[1][2] = -sin_val;
    xform_matrix[2][0] = 0; xform_matrix[2][1] = sin_val; xform_matrix[2][2] = cos_val;
}

// Purpose: Assigns the y transformation matrix
void yrotation (xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0);
    double cos_val = cos(rad);
    double sin_val = sin(rad);

    xform_matrix[0][0] = cos_val; xform_matrix[0][1] = 0; xform_matrix[0][2] = sin_val;
    xform_matrix[1][0] = 0; xform_matrix[1][1] = 1; xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin_val; xform_matrix[2][1] = 0; xform_matrix[2][2] = cos_val;
}

// Purpose: Assigns the z transformation matrix
void zrotation (xform_matrix xform_matrix, unsigned short deg){
    double rad = deg * (M_PI / 180.0);
    double cos_val = cos(rad);
    double sin_val = sin(rad);

    xform_matrix[0][0] = cos_val; xform_matrix[0][1] = -sin_val; xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin_val; xform_matrix[1][1] = cos_val; xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0; xform_matrix[2][1] = 0; xform_matrix[2][2] = 1;
}

// Purpose: perform matrix multiplication to the atom vectors, implementing rotation
void mol_xform (molecule *molecule, xform_matrix matrix){

    if (molecule == NULL){
        return;
    }

    double x_vector, y_vector, z_vector;

    for (int i = 0; i < molecule->atom_no; i++){
        // store in separate variable to avoid reassignment during calculation
        x_vector = molecule->atoms[i].x;
        y_vector = molecule->atoms[i].y;
        z_vector = molecule->atoms[i].z;

        molecule->atoms[i].x = matrix[0][0] * x_vector + matrix[0][1] * y_vector + matrix[0][2] * z_vector;
        molecule->atoms[i].y = matrix[1][0] * x_vector + matrix[1][1] * y_vector + matrix[1][2] * z_vector;
        molecule->atoms[i].z = matrix[2][0] * x_vector + matrix[2][1] * y_vector + matrix[2][2] * z_vector;

    }

    // Update the bond values with the atom values
    for (int i = 0; i < molecule->bond_no; i++){
        compute_coords(&molecule->bonds[i]);
    }
}

// compares two z values from two atoms
int cmpfunc_atom (const void *a, const void *b){
    struct atom *a_atom, *b_atom;

    // We passed in two double pointers because they point to the address of the
    // the elements in the array, which is a struct atom pointer. We dereference
    // to get the individual element as a pointer.
    a_atom = *(struct atom **)a;
    b_atom = *(struct atom **)b;

    return (int)((a_atom->z > b_atom->z) - (a_atom->z < b_atom->z));
}

// compares two z values from two bonds
int cmpfunc_bond (const void *a, const void *b){
    struct bond *a_bond, *b_bond;

    a_bond = *(struct bond **)a;
    b_bond = *(struct bond **)b;

    return (int)((a_bond->z > b_bond->z) - (a_bond->z < b_bond->z));
}

// should compute all coordinate values
void compute_coords(bond *bond){
    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;

    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;

    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;

    bond->len = sqrt(pow(bond->x2 - bond->x1, 2) + pow(bond->y2 - bond->y1, 2));

    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;
}


