import sqlite3
from Globals import DATABASE_NAME

connection = sqlite3.connect(DATABASE_NAME)

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.close()
