import os
import sqlite3
import MolDisplay

# pretty print - REMOVE before submission
def pp( listoftuples ):
    columns = len(listoftuples[0]);
    widths = [ max( [ len(str(item[col])) for item in listoftuples ] ) \
                                for col in range( columns ) ];

    fmt = " | ".join( ["%%-%ds"%width for width in widths] );
    for row in listoftuples:
        print( fmt % row );

class Database:
    def __init__( self, reset=False ):

        # for testing - ensures db creation is consistent
        if reset == True:
            os.remove( 'molecules.db' )

        # create database file if it doesn't exist and connect to it
        conn = sqlite3.connect( 'molecules.db' )
        self.conn = conn

    def create_tables( self ):

        # Function to confirm if table is empty
        def fetch_name(table_name):
            string = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            sql = self.conn.execute(string)
            result = sql.fetchall()

            return len(result)

        ### ALL SQL TABLES ###

        # check if table is empty -> create it
        if fetch_name('Elements') is 0: 
            self.conn.execute( """CREATE TABLE Elements 
            (   ELEMENT_NO       INTEGER NOT NULL,
                ELEMENT_CODE     VARCHAR(3) PRIMARY KEY NOT NULL,
                ELEMENT_NAME     VARCHAR(32) NOT NULL,
                COLOUR1          CHAR(6) NOT NULL,
                COLOUR2          CHAR(6) NOT NULL,
                COLOUR3          CHAR(6) NOT NULL,
                RADIUS           DECIMAL(3) NOT NULL )""" )

        if fetch_name('Atoms') is 0:
            self.conn.execute( """CREATE TABLE Atoms 
            (   ATOM_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ELEMENT_CODE     VARCHAR(32)  NOT NULL,
                X                DECIMAL(7,4)  NOT NULL,
                Y                DECIMAL(7,4)  NOT NULL,
                Z                DECIMAL(7,4)  NOT NULL,
                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements )""" )

        if fetch_name('Bonds') is 0:
            self.conn.execute( """CREATE TABLE Bonds 
            (   BOND_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                A1               INTEGER NOT NULL,
                A2               INTEGER NOT NULL,
                EPAIRS           INTEGER NOT NULL )""" )

        if fetch_name('Molecules') is 0:
            self.conn.execute( """CREATE TABLE Molecules 
            (   MOLECULE_ID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME             TEXT NOT NULL UNIQUE )""" )

        if fetch_name('MoleculeAtom') is 0:                
            self.conn.execute( """CREATE TABLE MoleculeAtom
            (   MOLECULE_ID      INTEGER NOT NULL,
                ATOM_ID          INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, ATOM_ID), 
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID) )""" )

        if fetch_name('MoleculeBond') is 0:
            self.conn.execute( """CREATE TABLE MoleculeBond
            (   MOLECULE_ID      INTEGER NOT NULL,
                BOND_ID          INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID) )""" )

    # edge case of whether the amount of correct values have been added
    # could get indexing err
    def __setitem__( self, table, values ):

        columns = []

        # Based on table get all columns
        data = self.conn.execute(f"""
        PRAGMA table_info({table})""")
        arr = data.fetchall()

        ## NOT PRAGMA - harder
        # columns = self.conn.execute(f""" 
        # SELECT sql FROM sqlite_master WHERE 
        # type='table' AND tbl_name='{table}'""")
        
        # get all column names
        for entry in arr:
            columns.append(entry[1])

        # make list values into a string
        s_columns = ', '.join(columns)
        
        self.conn.execute(f"""
        INSERT INTO {table}({s_columns}) VALUES {values}""")


        ## TEST TO ENSURE WORKS CORRECTLY
        # pp( self.conn.execute( f"""SELECT * FROM {table}""" ).fetchall() )
        # print()


    # assuming atom is the atom object 
    # ID is autoincrement for both molecule and atom
    # molname is given to fill molname
    def add_atom( self, molname, atom):

        ## insert into atom table
        self.conn.execute(f"""
        INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z) 
        VALUES ('{atom.element}', {atom.x}, {atom.y}, {atom.z}) """)

        ## insert into molecule table - MISTAKE
        # self.conn.execute(f"""
        # INSERT INTO Molecules (NAME) 
        # VALUES ('{molname}')""")

        # Get the atom and molecule id
        atom_id = self.conn.execute(f"""
        SELECT last_insert_rowid() FROM Atoms""").fetchone()[0]
        # print(atom_id)

        mol_id = self.conn.execute(f"""
        SELECT MOLECULE_ID FROM Molecules ORDER BY MOLECULE_ID DESC LIMIT 1""").fetchone()[0]
        # print(mol_id)

        ## insert into moleculeatom table
        self.conn.execute(f"""
        INSERT INTO MoleculeAtom (ATOM_ID, MOLECULE_ID)
        VALUES ({atom_id}, {mol_id})""")

        # pp( self.conn.execute( f"""SELECT * FROM MoleculeAtom""" ).fetchall() )

    def add_bond( self, molname, bond):

        ## insert into bond table
        self.conn.execute(f"""
        INSERT INTO Bonds(A1, A2, EPAIRS) 
        VALUES ('{bond.a1}', {bond.a2}, {bond.epairs} )""")

        ## insert into molecule table
        # self.conn.execute(f"""
        # INSERT INTO Molecules (NAME) 
        # VALUES ('{molname}')""")

        # Get the bond and molecule id
        bond_id = self.conn.execute(f"""
        SELECT last_insert_rowid() FROM Bonds""").fetchone()[0]
        # print(bond_id)

        mol_id = self.conn.execute(f"""
        SELECT MOLECULE_ID FROM Molecules ORDER BY MOLECULE_ID DESC LIMIT 1""").fetchone()[0]
        # print(mol_id.fetchone()) - TEST

        ## insert into moleculebond table
        self.conn.execute(f"""
        INSERT INTO MoleculeBond (BOND_ID, MOLECULE_ID)
        VALUES ({bond_id}, {mol_id})""")

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

    # temporary
    def close( self ):
        self.conn.close()
        
def main():
    db = Database(reset=True)
    db.create_tables()

    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );

    ## INDIVIDUAL TEST FOR ADD_ATOM ##
    # mol = MolDisplay.Molecule()
    # mol.append_atom("O", 2.5369, -0.1550, 1.5000)
    
    # atom = MolDisplay.Atom(mol.get_atom(0))
    # db.add_atom('Water', atom)

    fp = open( 'water-3D-structure-CT1000292221.sdf' );
    db.add_molecule( 'Water', fp );
    fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    db.add_molecule( 'Caffeine', fp );
    fp = open( 'CID_31260.sdf' );
    db.add_molecule( 'Isopentanol', fp );
    
    # display tables
    pp( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    print()
    pp( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    print()
    pp( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    print()
    pp( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    print()
    pp( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    print()
    pp( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );

    db.close()

if __name__ == "__main__":
    main()
