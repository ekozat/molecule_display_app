import os
import sqlite3

# for testing only; remove this for real usage
if os.path.exists( 'test.db' ):
    os.remove( 'test.db' )

# create database file if it doesn't exist and connect to it
conn = sqlite3.connect( 'test.db' )

### ALL SQL TABLES ###

conn.execute( """CREATE TABLE Elements 
                 ( ELEMENT_NO       INTEGER NOT NULL,
                   ELEMENT_CODE     VARCHAR(3) NOT NULL,
                   ELEMENT_NAME     VARCHAR(32) NOT NULL,
                   COLOUR1          CHAR(6) NOT NULL,
                   COLOUR2          CHAR(6) NOT NULL,
                   COLOUR3          CHAR(6) NOT NULL,
                   RADIUS           DECIMAL(3) NOT NULL,
                   PRIMARY KEY (ELEMENT_CODE) )""" )

conn.execute( """CREATE TABLE Atoms 
                 ( ATOM_ID          INTEGER  NOT NULL AUTO_INCREMENT,
                   ELEMENT_CODE     VARCHAR(32)  NOT NULL,
                   X                DECIMAL(7,4)  NOT NULL,
                   Y                DECIMAL(7,4)  NOT NULL,
                   Z                DECIMAL(7,4)  NOT NULL,
                   PRIMARY KEY (ATOM_ID) )
                   FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements""" )


conn.execute( """CREATE TABLE Bonds 
                 ( BOND_ID          INTEGER NOT NULL AUTO_INCREMENT,
                   A1               INTEGER NOT NULL,
                   EPAIRS           INTEGER NOT NULL,
                   PRIMARY KEY (BOND_ID) )""" )

conn.execute( """CREATE TABLE Molecules 
                 ( MOLECULE_ID      INTEGER NOT NULL AUTO_INCREMENT,
                   NAME             TEXT NOT NULL,
                   PRIMARY KEY (MOLECULE_ID) )""" )

                   
conn.execute( """CREATE TABLE MoleculeAtom
                 ( MOLECULE_ID      INTEGER NOT NULL,
                   ATOM_ID          INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID) )
                   PRIMARY KEY (ATOM_ID) )
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules )
                   FOREIGN KEY (ATOM_ID) ) REFERENCES Atoms""" )

conn.execute( """CREATE TABLE MoleculeBond
                 ( MOLECULE_ID      INTEGER NOT NULL,
                   BOND_ID          INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID) )
                   PRIMARY KEY (BOND_ID) )
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules )
                   FOREIGN KEY (BOND_ID) ) REFERENCES Bonds""" )
