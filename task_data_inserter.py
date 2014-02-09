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
              'id integer primary key autoincrement,' \
              'query text,' \
              'url text,' \
              'noun text,' \
              'cmp text,' \
              'verb text' \
              ');'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()


    def has(self, query, url, noun, cmp, verb):
        sql = 'select * from  tasks where exists(' \
              'select * from  tasks where query = "%s" and url = "%s" and noun = "%s" and cmp = "%s" and verb = "%s"' \
              ')' % (query, url, noun, cmp, verb)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            return False
        if self.cur.fetchall():
            return True
        return False

    def insert(self, query, url, noun, cmp, verb):
        if self.has(query, url, noun, cmp, verb):
            print('%sのタスクはすでに存在しているのでスキップしました' % url)
            return False
        try:
            sql = 'insert into tasks(query, url, noun, cmp, verb) values("%s", "%s", "%s", "%s", "%s")' \
                  % (query, url, noun, cmp, verb)
        except IndexError:
            print('%sのタスクのinsert失敗' % url)
            return False
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%sの入力完了！' % url)
        self.conn.commit()

