# -*- coding: utf-8 -*-
import pdb
import numpy
import sqlite3
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class TaskDataSelector(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, db_name='tasks.sqlite', table_name='tasks'):
        super().__init__(db_name, table_name)

    def id_with_url_noun_cmp_verb(self, url, noun, cmp, verb):
        sql = 'select tasks.id from tasks, pages ' \
              'where pages.id = tasks.page_id ' \
              'and pages.url = "%s" ' \
              'and tasks.noun = "%s" ' \
              'and tasks.cmp = "%s" ' \
              'and tasks.verb = "%s";' % (url, noun, cmp, verb)
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchone()
        pdb.set_trace()
        return results

    def num_of_queries_contain_noun(self, noun):
        sql = 'select count(distinct pages.query) from tasks, sentences, pages ' \
              'where noun = "%s" ' \
              'and tasks.sentence_id = sentences.id ' \
              'and pages.id = sentences.page_id;' % noun
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        result = self.cur.fetchone()  #数字
        return int(result[0])

    def num_of_queries_contain_ncv(self, noun, cmp, verb):
        sql = 'select count(distinct pages.query) from tasks, pages, sentences where ' \
              'tasks.noun = "%s" and ' \
              'tasks.cmp = "%s" and ' \
              'tasks.verb = "%s" and ' \
              'tasks.sentence_id = sentences.id ' \
              'and pages.id = sentences.page_id;' % (noun, cmp, verb)
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        result = self.cur.fetchone()  #数字
        return int(result[0])

    def num_of_queries(self):
        sql = 'select count(distinct pages.query) from tasks, sentences, pages ' \
              'where tasks.sentence_id = sentences.id ' \
              'and pages.id = sentences.page_id;'
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        result = self.cur.fetchone()  #数字
        return result[0]

    def tasks_with_query(self, query, rank_threshold=100):
        sql = 'select distinct tasks.noun, tasks.cmp, tasks.verb, pages.rank, subtype_nouns.body ' \
              'from tasks, sentences, pages, sentence_subtype, subtype_nouns ' \
              'where tasks.sentence_id = sentences.id ' \
              'and sentences.page_id = pages.id ' \
              'and sentences.id = sentence_subtype.sentence_id ' \
              'and sentence_subtype.subtype_id = subtype_nouns.id ' \
              'and pages.rank < %i ' \
              'and query = "%s";' % (rank_threshold, query)
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchall()
        pdb.set_trace()
        # ('栽培方法', 'を', '参考する', 97), ('たくさん道ばた', 'に', '落ちる', 98), ...]
        return results

    def task_ids_with_query(self, query):
        sql = 'select distinct tasks.id ' \
              'from tasks, sentences, pages ' \
              'where tasks.sentence_id = sentences.id ' \
              'and sentences.page_id = pages.id ' \
              'and pages.query = "%s";' % query
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchall()
        return [result[0] for result in results]


    def tasks_of_subtype_with_query(self, query, rank_threshold=100):
        sql = 'select distinct tasks.noun, tasks.cmp, tasks.verb, pages.url, pages.rank, subtype_nouns.body, ' \
              'sentences.sequence, sentence_subtype.sentence_id ' \
              'from tasks, sentences, pages, sentence_subtype, subtype_nouns ' \
              'where tasks.sentence_id = sentences.id ' \
              'and sentences.page_id = pages.id ' \
              'and sentences.id = sentence_subtype.sentence_id ' \
              'and sentence_subtype.subtype_id = subtype_nouns.id ' \
              'and pages.rank < %i ' \
              'and query = "%s";' % (rank_threshold, query)
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchall()
        pdb.set_trace()
        return results

    def subtype_ids_with_task_id(self, task_id):
        # task_idのページidをまず探す
        page_id = self.page_id_with_task_id(task_id)
        sql = 'select subtype_nouns.id ' \
              'from subtype_nouns, sentences, sentence_subtype, pages ' \
              'where subtype_nouns.id = sentence_subtype.subtype_id ' \
              'and sentences.id = sentence_subtype.sentence_id ' \
              'and sentences.page_id = pages.id ' \
              'and pages.id = %i;' % page_id
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchall()
        if results:
            return [result[0] for result in results]
        return 0  #Falseということ

    def page_id_with_task_id(self, task_id):
        sql = 'select pages.id ' \
              'from pages, sentences, tasks ' \
              'where pages.id = sentences.page_id ' \
              'and sentences.id = tasks.sentence_id ' \
              'and tasks.id = %i;' % task_id
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchone()
        if results:
            return results[0]
        return 0  #Falseということ

    def subtype_sentence_sequence(self, subtype_id):
        sql = 'select sentences.sequence ' \
              'from sentences, sentence_subtype ' \
              'where sentence_subtype.sentence_id = sentences.id ' \
              'and sentence_subtype.subtype_id = %i;' % subtype_id
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchone()
        if results:
            return results[0]
        return 0  #Falseということ

    def task_sentence_sequence(self, task_id):
        sql = 'select sentences.sequence ' \
              'from sentences, tasks ' \
              'where tasks.sentence_id = sentences.id ' \
              'and tasks.id = %i;' % task_id
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchone()
        if results:
            return results[0]
        return 0  #Falseということ

    def taskdata_with_task_id(self, task_id):
        sql = 'select tasks.noun, tasks.cmp, tasks.verb, sentences.sequence, pages.query, pages.url, pages.rank ' \
              'from tasks, sentences, pages ' \
              'where tasks.sentence_id = sentences.id ' \
              'and sentences.page_id = pages.id ' \
              'and tasks.id = %i;' % task_id
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchall()
        if results:
            return results[0]
        return 0  #Falseということ

class Median:
    def __init__(self):
        self.values = []
    def step(self, value):
        self.values.append(value)
    def finalize(self):
        return numpy.median(self.values)


if __name__ == '__main__':
    with TaskDataSelector() as selector:
        for i in range(10000):
            subtype_ids = selector.subtype_ids_with_task_id(i+1)
