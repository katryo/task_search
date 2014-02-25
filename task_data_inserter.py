# -*- coding: utf-8 -*-
import sqlite3
import pdb
from base_sqlite_manager import BaseSQLiteManager

class TaskDataInserter(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='tasks'):
        super().__init__(db_name, table_name)
        self._create_table()

    def _create_table(self):
        sql = 'create table if not exists tasks(' \
              'id integer primary key autoincrement, ' \
              'sentence_id integer, ' \
              'noun text, ' \
              'cmp text, ' \
              'verb text, ' \
              'unique(sentence_id)' \
              ');'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()


    def has(self, sentence_id, noun, cmp, verb):
        sql = 'select * from  tasks where exists(' \
              'select * from  tasks where sentence_id = %i and noun = "%s" and cmp = "%s" and verb = "%s"' \
              ')' % (sentence_id, noun, cmp, verb)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            return False
        if self.cur.fetchall():
            return True
        return False

    def insert(self, sentence_id, noun, cmp, verb):
        if self.has(sentence_id, noun, cmp, verb):
            print('%iのタスクはすでに存在しているのでスキップしました' % sentence_id)
            return False
        try:
            sql = 'insert into tasks(sentence_id, noun, cmp, verb) values(%i, "%s", "%s", "%s")' \
                  % (sentence_id, noun, cmp, verb)
        except IndexError:
            print('%iのタスクのinsert失敗' % sentence_id)
            return False
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%iの入力完了！' % sentence_id)
        self.conn.commit()

