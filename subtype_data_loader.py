# -*- coding: utf-8 -*-
import sqlite3
import pdb
from base_sqlite_manager import BaseSQLiteManager

class SubtypeDataLoader(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='subtype_nouns'):
        super().__init__(db_name, table_name)

    def bodies_with_supertype_noun(self, supertype_noun):
        sql = 'select body from subtype_nouns where supertype_noun = "%s";' % supertype_noun
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        bodies = self.cur.fetchall()
        if not bodies:
            raise EOFError
        return bodies

    def id_with_body(self, body):
        sql = 'select id from subtype_nouns where body = "%s";' % body
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        id = self.cur.fetchone()
        if not id:
            pdb.set_trace()
            raise EOFError
        return id[0]
