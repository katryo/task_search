import sqlite3
import pdb

class BaseSQLiteManager(object):
    def __init__(self, db_name='', table_name=''):
        self.conn = sqlite3.connect(db_name)
        self.table_name = table_name
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        self.conn.close()

    def __del__(self):
        self.conn.close()