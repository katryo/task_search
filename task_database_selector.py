# -*- coding: utf-8 -*-
import pdb
import numpy
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class TaskDatabaseSelector(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, db_name='tasks.sqlite', table_name='tasks'):
        super().__init__(db_name, table_name)

    def num_of_queries_contain_noun(self, noun):
        sql = 'select count(distinct query) from tasks where noun = "%s"' % noun
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        result = self.cur.fetchone()  #数字
        return int(result[0])

    def num_of_queries_contain_ncv(self, noun, cmp, verb):
        sql = 'select count(distinct query) from tasks where ' \
              'noun = "%s" and ' \
              'cmp = "%s" and ' \
              'verb = "%s"' % (noun, cmp, verb)
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        result = self.cur.fetchone()  #数字
        return int(result[0])

    def num_of_queries(self):
        sql = 'select count(distinct query) from tasks'
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        result = self.cur.fetchone()  #数字
        return result[0]


class Median:
    def __init__(self):
        self.values = []
    def step(self, value):
        self.values.append(value)
    def finalize(self):
        return numpy.median(self.values)