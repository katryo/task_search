# -*- coding: utf-8 -*-
import pdb
import numpy
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class TaskDataSelector(BaseSQLiteManager, SQLiteDataLoadable):
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

    def task_set_of_higher_rank_with_query(self, query, rank_threshold=100):
        sql = 'select tasks.noun, tasks.cmp, tasks.verb, pages.rank from tasks, sentences, pages ' \
              'where tasks.sentence_id = sentences.id and sentences.page_id = pages.id ' \
              'and pages.rank < %i and query = "%s";' % (rank_threshold, query)
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        results = self.cur.fetchall()
        # ('栽培方法', 'を', '参考する', 97), ('たくさん道ばた', 'に', '落ちる', 98), ...]
        return results


class Median:
    def __init__(self):
        self.values = []
    def step(self, value):
        self.values.append(value)
    def finalize(self):
        return numpy.median(self.values)