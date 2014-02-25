# -*- coding: utf-8 -*-
import sqlite3
import pdb
from base_sqlite_manager import BaseSQLiteManager

class PageDataLoader(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='pages'):
        super().__init__(db_name, table_name)

    def body_with_id(self, page_id):
        sql = 'select body from pages where id = %i;' % page_id
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        body = self.cur.fetchone()
        if not body:
            raise EOFError
        return body[0]
