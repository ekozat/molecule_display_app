//asks if _mol_h is defined. If not defined, executes everything if statement (the entire header file)
//if already defined, doesn't enter the if statement and exits. Ensures that the same header file doesn't get 
//stored in memory twice. Happens in nested header files
#ifndef _mol_h
#define _mol_h

#define M_PI 3.14159265358979323846264338

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//describes an atom and its position
typedef struct atom
{
    char element[3]; //element name
    double x, y, z; //position
}atom;

//describes covalent bond b/w 2 atoms
//NOTE: no need to free a1, a2
typedef struct bond
{
    atom *a1, *a2; //Bond between the two atoms
    unsigned char epairs; //number of electron pairs
}bond;

//represents molecule holding 0+ atoms and 0+ bonds
typedef struct molecule 
{
    unsigned short atom_max, atom_no; 
    atom *atoms, **atom_ptrs; 
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
}molecule;

typedef double xform_matrix[3][3];

//FUNCTIONS
void atomset (atom *atom, char element[3], double *x, double *y, double *z);
void atomget (atom *atom, char element[3], double *x, double *y, double *z);
void bondset (bond *bond, atom *a1, atom *a2, unsigned char epairs);
void bondget (bond *bond, atom **a1, atom **a2, unsigned char *epairs);
molecule *molmalloc (unsigned short atom_max, unsigned short bond_max);
molecule *molcopy (molecule *src);
void molfree (molecule *ptr);
void molappend_atom (molecule *molecule, atom *atom);
void molappend_bond (molecule *molecule, bond *bond);
void molsort (molecule *molecule);
void xrotation (xform_matrix xform_matrix, unsigned short deg);
void yrotation (xform_matrix xform_matrix, unsigned short deg);
void zrotation (xform_matrix xform_matrix, unsigned short deg);
void mol_xform (molecule *molecule, xform_matrix matrix);

// helper functions
int cmpfunc_atom (const void *a, const void *b);
int cmpfunc_bond (const void *a, const void *b);
#endif
