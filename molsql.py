import os
import sqlite3

# for testing only; remove this for real usage
if os.path.exists( 'test.db' ):
    os.remove( 'test.db' )

# create database file if it doesn't exist and connect to it
conn = sqlite3.connect( 'test.db' )


