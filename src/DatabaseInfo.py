# https://docs.python.org/3/library/sqlite3.html
import sqlite3
from typing import Optional, Tuple, List
import os
import sys
from EncryptDatabase import EncryptDatabase

class DatabaseInfo:
    def __init__(self):
        self.con = sqlite3.connect('drive.db')
        self.cur = self.con.cursor()
        self.encryption = EncryptDatabase()



    def __del__(self):
        self.con.close()



    def config_init(self) -> None:
        # open the sql file containing definitions and read execute it
        with open('src/sql/drive_info.sql', 'r') as file:
            sql_script = file.read()
        try:
            self.cur.executescript(sql_script)
        except Exception as e:
            print(f"An error occured: {e}\nCancelling...")
            os.remove('drive.db')
            sys.exit(-2)



    def config_add(self, name : str, path : str) -> None:
        # encrypt password data
        password = self.encryption.create_password()
        pwd_enc = self.encryption.store_password(password)
        self.encryption.load_password(pwd_enc)

        # insert the data into database
        self.cur.execute('INSERT INTO databpwd(password, salt) VALUES (?, ?)', (pwd_enc[0], pwd_enc[1]))

        # fetch the last insertion
        databpwd_id = self.cur.lastrowid
        self.cur.execute('SELECT * FROM databpwd WHERE id = ?', (databpwd_id,))
        pwd_data = self.cur.fetchone()

        # insert data to drive table 
        path_enc = self.encryption.encrypt_data(path)
        self.cur.execute('INSERT INTO drive(name, path, current, databpwd_id) VALUES (?, ?, 0, ?)', (name, path_enc, databpwd_id))
        self.con.commit()


    
    def config_fetch_specific(self, name: str) -> Optional[Tuple[int, str, bytes, int, int]]:

        self.cur.execute('SELECT * FROM drive WHERE name = ?', (name,))
        data = self.cur.fetchone()
        if data:
            return data
        else:
            return None



    # should add a view for this
    def config_fetch_current(self) -> Optional[Tuple[str, str, int]]:
        self.cur.execute('SELECT * FROM drive WHERE current = 1')
        data = self.cur.fetchone()
        if data:
            return data
        else: return None
    


    def config_switch_current(self, name : str):
        self.cur.execute("""
            UPDATE drive
            SET current = CASE
                WHEN current = 0 THEN 1
                ELSE 0
            END
            WHERE name = ?;
        """, (name,))
        self.con.commit()



    def pretty_print_names(self) -> None:
        self.cur.execute('SELECT * FROM drive')
        drives = self.cur.fetchall()

        # in case there is no target
        if not drives:
            sys.exit(0)

        
        # get the max length of of the Name
        str1_max = max(len(item[1]) for item in drives)
        str1_max = max(str1_max, len('Name'))

        # colors to highlight current
        RED = "\033[31m"
        RESET = "\033[0m"

        # output
        print(f"{'Name'.ljust(str1_max)}\n")
        for item in drives:
            if item[3] == 0:
                print(f"{item[1].ljust(str1_max)}")
            elif item[3] == 1:
                print(f"{RED}{item[1].ljust(str1_max)}{RESET}")



    def config_remove(self, name : str) -> None:
        if not self.encryption.key:
            print('Could not remove drive from database')
            sys.exit(-2)

        self.cur.execute('DELETE FROM drive WHERE name = ?', (name,))
        self.con.commit()



    def get_password(self, id : int) -> Optional[Tuple[bytes, bytes]]:
        self.cur.execute('SELECT password, salt FROM databpwd WHERE id = ?', (id,))
        return self.cur.fetchone()