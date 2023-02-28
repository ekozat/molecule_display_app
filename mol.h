/*
 Student Name: Emily Kozatchiner
 Student ID: 1149665
 Due Date: Jan 30, 2023
 Course: CIS*2750
 I have exclusive control over this submission via my password.
 By including this header comment, I certify that I have read and understood 
 the policy on academic integrity. I assert that this work is my own. 
 I have appropriate acknowledged any and all material that I have used, 
 be it directly quoted or paraphrased. Furthermore, I certify that this 
 assignment was written by me in its entirety.
*/

// Before compiling, please execute: export LD_LIBRARY_PATH=.
// Compilation: make
// Running: ./myprog

#ifndef _mol_h
#define _mol_h

#define M_PI 3.14159265358979323846264338

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// describes an atom and its position
typedef struct atom
{
    char element[3];
    double x, y, z; 
}atom;

typedef struct bond
{
    unsigned short a1, a2; // indices of the two atoms in the array (change)
    unsigned char epairs; // stays the same as before
    atom *atoms; // holds entire array of the atoms
    double x1, x2, y1, y2, z, len, dx, dy; // instead of holding the doubles in the atom struct, we will hold them in the bond struct.

} bond;

// represents molecule holding 0+ atoms and 0+ bonds
typedef struct molecule 
{
    unsigned short atom_max, atom_no; 
    atom *atoms, **atom_ptrs; 
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
}molecule;

// transformation matrix for molecule rotation
typedef double xform_matrix[3][3];

// Functions
void atomset (atom *atom, char element[3], double *x, double *y, double *z);
void atomget (atom *atom, char element[3], double *x, double *y, double *z);
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);
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
void compute_coords (bond *bond);

// Helper functions
int cmpfunc_atom (const void *a, const void *b);
int cmpfunc_bond (const void *a, const void *b);
#endif
