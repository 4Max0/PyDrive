# https://docs.python.org/3/library/sqlite3.html
import sqlite3
import pathlib

# needs to be implemented
class Database:

    def __init__(self):
        pass

    def __del__(self):
        pass

    def init_database(self, path : pathlib.Path) -> None:
        con = sqlite3.connect( str(path / 'datab.db' ))
        cur = con.cursor()
        # cur.execute('CREATE TABLE file(filename, filepath)')
        con.commit()
        con.close()