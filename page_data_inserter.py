# -*- coding: utf-8 -*-
import sqlite3
import pdb
from base_sqlite_manager import BaseSQLiteManager

class PageDataInserter(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='pages'):
        super().__init__(db_name, table_name)
        self._create_table()

    def _create_table(self):
        sql = 'create table if not exists pages(' \
              'id integer primary key autoincrement,' \
              'title text,' \
              'snippet text,' \
              'body text,' \
              'html text,' \
              'query text,' \
              'url text,' \
              'rank integer' \
              ');'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()


    def has(self, query, url):
        sql = 'select * from pages where exists(' \
              'select * from pages where url = "%s" and query = "%s"' \
              ')' % (url, query)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            return False
        if self.cur.fetchall():
            print('もうdbにあります')
            return True
        return False

    def insert(self, query, url, title, snippet, rank):
        if self.has(query, url):
            print('%sのページはすでに存在しているのでスキップしました' % url)
            return False
        try:
            sql = 'insert into pages(title, snippet, url, query, rank) ' \
                  'values("%s", "%s", "%s", "%s", %i)' \
                  % (title, snippet, url, query, rank)
        except IndexError:
            print('%sのタスクのinsert失敗' % url)
            return False
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%sの入力完了！' % url)
        self.conn.commit()

    def update_body(self, body, url):
        sql = 'update pages set body = "%s" where url = "%s"' % (body, url)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except sqlite3.OperationalError:
            print('bodyのsetに失敗しました')

    def has_body(self, query, url):
        sql = 'select body from pages where query = "%s" and url = "%s"' % (query, url)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            return False
        answer = self.cur.fetchone()
        print(answer[0])
        if answer[0]:
            print('%sはbodyがあります' % url)
            return True
        return False
