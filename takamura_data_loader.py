# -*- coding: utf-8 -*-
import pdb
import numpy
import sqlite3
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class TakamuraDataLoader(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, db_name='takamura_dict.sqlite', table_name='terms'):
        super().__init__(db_name, table_name)

    def score_with_term(self, term):
        sql = 'select score from terms where kanji = "%s"' % term
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchone()
        if results:
            return results[0]
        return 0.0


