# -*- coding: utf-8 -*-
import pdb
import numpy
import sqlite3
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class EvaluationDictDataLoader(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, db_name='evaluation_dict.sqlite', table_name='terms'):
        super().__init__(db_name, table_name)

    def positive_experiences(self):
        sql = 'select terms_text from terms where category = "ポジ（経験）";'
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        sql_results = self.cur.fetchall()
        results = [result[0].rstrip() for result in sql_results]
        if results:
            return [result for result in results if result]
        return []


    def score_with_terms_text(self, stems_text):
        sql = 'select * from terms where category = "ポジ（経験）" and ' \
              'terms_text = "%s" limit 1;' % stems_text
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchall()
        if results:
            pdb.set_trace()
            return results[0]
        return 0.0


if __name__ == '__main__':
    with EvaluationDictDataLoader() as loader:
        loader.positive_experiences()