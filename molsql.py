import os
import sqlite3

class Database:
    def __init__( self, reset=False ):

        # for testing - ensures db creation is consistent
        if reset == True:
            os.remove( 'molecules.db' )

        # create database file if it doesn't exist and connect to it
        conn = sqlite3.connect( 'molecules.db' )
        self.conn = conn

    def create_tables( self ):

        # Function to get the tables name
        def fetch_name(table_name):
            string = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            sql = self.conn.execute(string)
            result = sql.fetchall()

            return result


        ### ALL SQL TABLES ###

        if fetch_name('Elements') is None: 
            self.conn.execute( """CREATE TABLE Elements 
            (   ELEMENT_NO       INTEGER NOT NULL,
                ELEMENT_CODE     VARCHAR(3) PRIMARY KEY NOT NULL,
                ELEMENT_NAME     VARCHAR(32) NOT NULL,
                COLOUR1          CHAR(6) NOT NULL,
                COLOUR2          CHAR(6) NOT NULL,
                COLOUR3          CHAR(6) NOT NULL,
                RADIUS           DECIMAL(3) NOT NULL )""" )

        if fetch_name('Atoms') is None:
            self.conn.execute( """CREATE TABLE Atoms 
            (   ATOM_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ELEMENT_CODE     VARCHAR(32)  NOT NULL,
                X                DECIMAL(7,4)  NOT NULL,
                Y                DECIMAL(7,4)  NOT NULL,
                Z                DECIMAL(7,4)  NOT NULL,
                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements )""" )

        if fetch_name('Bonds') is None:
            self.conn.execute( """CREATE TABLE Bonds 
            (   BOND_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                A1               INTEGER NOT NULL,
                EPAIRS           INTEGER NOT NULL )""" )

        if fetch_name('Molecules') is None:
            self.conn.execute( """CREATE TABLE Molecules 
            (   MOLECULE_ID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME             TEXT NOT NULL UNIQUE )""" )

        if fetch_name('MoleculeAtom') is None:                
            self.conn.execute( """CREATE TABLE MoleculeAtom
            (   MOLECULE_ID      INTEGER NOT NULL,
                ATOM_ID          INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID) 
                PRIMARY KEY (ATOM_ID) )
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules )
                FOREIGN KEY (ATOM_ID) ) REFERENCES Atoms)""" )

            self.conn.execute( """CREATE TABLE MoleculeBond
            (   MOLECULE_ID      INTEGER NOT NULL,
                BOND_ID          INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID) 
                PRIMARY KEY (BOND_ID) )
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules )
                FOREIGN KEY (BOND_ID) ) REFERENCES Bonds)""" )
        
def main():
    db = Database(reset=True)
    db.create_tables()

if __name__ == "__main__":
    main()
