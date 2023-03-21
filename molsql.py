import os
import sqlite3
import MolDisplay

class Database:
    def __init__( self, reset=False ):

        # for testing - ensures db creation is consistent
        if reset == True:
            os.remove( 'molecules.db' )

        # create database file if it doesn't exist and connect to it
        conn = sqlite3.connect( 'molecules.db' )
        self.conn = conn

    # Purpose: Create all database tables that will be filled
    def create_tables( self ):

        # Function to confirm if table is empty
        def fetch_name(table_name):
            string = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            sql = self.conn.execute(string)
            result = sql.fetchall()

            return len(result)

        ### ALL SQL TABLES ###

        # Creating Elements table
        if fetch_name('Elements') is 0: 
            self.conn.execute( """CREATE TABLE Elements 
            (   ELEMENT_NO       INTEGER NOT NULL,
                ELEMENT_CODE     VARCHAR(3) PRIMARY KEY NOT NULL,
                ELEMENT_NAME     VARCHAR(32) NOT NULL,
                COLOUR1          CHAR(6) NOT NULL,
                COLOUR2          CHAR(6) NOT NULL,
                COLOUR3          CHAR(6) NOT NULL,
                RADIUS           DECIMAL(3) NOT NULL )""" )

        # Creating Atoms table
        if fetch_name('Atoms') is 0:
            self.conn.execute( """CREATE TABLE Atoms 
            (   ATOM_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ELEMENT_CODE     VARCHAR(32)  NOT NULL,
                X                DECIMAL(7,4)  NOT NULL,
                Y                DECIMAL(7,4)  NOT NULL,
                Z                DECIMAL(7,4)  NOT NULL,
                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements )""" )

        # Creating Bonds table
        if fetch_name('Bonds') is 0:
            self.conn.execute( """CREATE TABLE Bonds 
            (   BOND_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                A1               INTEGER NOT NULL,
                A2               INTEGER NOT NULL,
                EPAIRS           INTEGER NOT NULL )""" )

        # Creating Molecules table
        if fetch_name('Molecules') is 0:
            self.conn.execute( """CREATE TABLE Molecules 
            (   MOLECULE_ID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME             TEXT NOT NULL UNIQUE )""" )

        # Creating MoleculeAtom relational table 
        if fetch_name('MoleculeAtom') is 0:                
            self.conn.execute( """CREATE TABLE MoleculeAtom
            (   MOLECULE_ID      INTEGER NOT NULL,
                ATOM_ID          INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, ATOM_ID), 
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID) )""" )

        # Creating MoleculeBond relational table
        if fetch_name('MoleculeBond') is 0:
            self.conn.execute( """CREATE TABLE MoleculeBond
            (   MOLECULE_ID      INTEGER NOT NULL,
                BOND_ID          INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID) )""" )

        # commit transaction to db
        self.conn.commit()

    # Purpose: provides indexing to set given values into given table 
    def __setitem__( self, table, values ):
        
        self.conn.execute(f"""
        INSERT INTO {table} VALUES {values}""")

        self.conn.commit()


    # Purpose: add a single atom into the database
    def add_atom( self, molname, atom):

        ## insert into atom table
        self.conn.execute(f"""
        INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z) 
        VALUES ('{atom.element}', {atom.x}, {atom.y}, {atom.z}) """)

        # Get the atom and molecule id
        atom_id = self.conn.execute(f"""
        SELECT last_insert_rowid() FROM Atoms""").fetchone()[0]

        mol_id = self.conn.execute(f"""
        SELECT MOLECULE_ID FROM Molecules ORDER BY MOLECULE_ID DESC LIMIT 1""").fetchone()[0]

        ## insert into moleculeatom table
        self.conn.execute(f"""
        INSERT INTO MoleculeAtom (ATOM_ID, MOLECULE_ID)
        VALUES ({atom_id}, {mol_id})""")

        self.conn.commit()

    # Purpose: Add a single bond into the database
    def add_bond( self, molname, bond):

        ## insert into bond table
        self.conn.execute(f"""
        INSERT INTO Bonds(A1, A2, EPAIRS) 
        VALUES ('{bond.a1}', {bond.a2}, {bond.epairs} )""")

        # Get the bond and molecule id
        bond_id = self.conn.execute(f"""
        SELECT last_insert_rowid() FROM Bonds""").fetchone()[0]

        mol_id = self.conn.execute(f"""
        SELECT MOLECULE_ID FROM Molecules ORDER BY MOLECULE_ID DESC LIMIT 1""").fetchone()[0]

        ## insert into moleculebond table
        self.conn.execute(f"""
        INSERT INTO MoleculeBond (BOND_ID, MOLECULE_ID)
        VALUES ({bond_id}, {mol_id})""")

        self.conn.commit()

    # Purpose: After parsing a given file and creating a molecule class,
    # the molecule should be added to the database alongside its atoms and bonds
    def add_molecule( self, name, fp):

        # create a molecule + parse the given file
        molecule = MolDisplay.Molecule()
        molecule.parse(fp)

        # add entry to the molecule table 
        self.conn.execute(f"""
        INSERT INTO Molecules (NAME)
        VALUES ('{name}')""")

        # Insert all atoms and bonds per molecule into db
        for i in range(molecule.atom_no):
            self.add_atom( name, molecule.get_atom(i))

        for i in range(molecule.bond_no):
            self.add_bond( name, molecule.get_bond(i))


        self.conn.commit()

    
    # Purpose: Reads all needed data from the database into the molecule object
    def load_mol( self, name ):
        molecule = MolDisplay.Molecule()

        # Get molecule ID
        id = self.conn.execute(f"""
        SELECT MOLECULE_ID FROM Molecules WHERE
        NAME='{name}'""").fetchone()[0]

        # Get all atoms associated to the molecule id
        atom_list = self.conn.execute(f"""
        SELECT * FROM Atoms INNER JOIN MoleculeAtom ON
        Atoms.ATOM_ID=MoleculeAtom.ATOM_ID AND
        MoleculeAtom.MOLECULE_ID={id}""").fetchall()

        # we need to fetch one at a time -> and insert into molecule via append_atom
        for atom in atom_list:
            molecule.append_atom(atom[1], atom[2], atom[3], atom[4])

        # Get all bonds associated to the molecule id
        bond_list = self.conn.execute(f"""
        SELECT * FROM Bonds INNER JOIN MoleculeBond ON
        Bonds.BOND_ID=MoleculeBond.BOND_ID AND
        MoleculeBond.MOLECULE_ID={id}""").fetchall()

        # fetch all bonds and insert into molecule
        for bond in bond_list:
            molecule.append_bond(bond[1], bond[2], bond[3])

        return molecule

    # Purpose: Returns a python dictionary mapping ELEMENT_CODE to RADIUS
    def radius ( self ):
        radius = {}

        arr = self.conn.execute(f"""
        SELECT ELEMENT_CODE, RADIUS FROM Elements""").fetchall()

        for element in arr:
            radius[element[0]] = element[1]

        return radius

    # Purpose: Returns a python dictionary mapping ELEMENT_CODE to ELEMENT_NAME
    def element_name ( self ):
        element_name = {}

        arr = self.conn.execute(f"""
        SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements""").fetchall()

        for element in arr:
            element_name[element[0]] = element[1]

        return element_name

    # Purpose: Combines all element svgs into one string constant and returns
    def radial_gradients( self ):

        # obtain all needed columns from all elements
        arr = self.conn.execute(f"""
        SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements""").fetchall()
        
        radialGradientSVG = ""
        
        # Combine svg strings with all elements
        for element in arr:
            radialGradientSVG += """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/>
                <stop offset="50%%" stop-color="#%s"/>
                <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (element[0], element[1], element[2], element[3])

        return radialGradientSVG
            
    # Purpose: closing database connection
    def close( self ):
        self.conn.close()
        
# def main():
#     db = Database(reset=True);
#     db.create_tables();
#     db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
#     db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
#     db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
#     db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
#     fp = open( 'water-3D-structure-CT1000292221.sdf' );
#     db.add_molecule( 'Water', fp );
#     fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
#     db.add_molecule( 'Caffeine', fp );
#     fp = open( 'CID_31260.sdf' );
#     db.add_molecule( 'Isopentanol', fp );
#     fp = open( 'ETHANE-3D-structure-CT1000156871.sdf' );
#     db.add_molecule( 'Ethane', fp );
#     # display tables
#     # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
#     # print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
#     # print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
#     # print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
#     # print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
#     # print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );
    
#     db = Database(reset=False); # or use default
#     MolDisplay.radius = db.radius();
#     MolDisplay.element_name = db.element_name();
#     MolDisplay.header += db.radial_gradients();

    

#     for molecule in [ 'Water', 'Caffeine', 'Isopentanol', 'Ethane' ]:
#         mol = db.load_mol( molecule );
#         mol.sort();
#         fp = open( molecule + ".svg", "w" );
#         fp.write( mol.svg() );
#         fp.close();


# if __name__ == "__main__":
#     main()
