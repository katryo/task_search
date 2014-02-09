# -*- coding: utf-8 -*-
import pdb
import numpy
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class TaskDatabaseSelector(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, db_name='tasks.sqlite', table_name='tasks'):
        super().__init__(db_name, table_name)

    def num_or_queries_contain_noun(self, noun):
        sql = 'select count(distinct query) from tasks where noun = "%s"' % noun
        self.cur.execute(sql)
        result = self.cur.fetchone()  #数字
        return int(result)

    def num_of_queries(self):
        sql = 'select count(distinct query)'
        self.cur.execute(sql)
        result = self.cur.fetchone()  #数字
        return int(result)


class Median:
    def __init__(self):
        self.values = []
    def step(self, value):
        self.values.append(value)
    def finalize(self):
        return numpy.median(self.values)