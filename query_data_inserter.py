# -*- coding: utf-8 -*-
import sqlite3
import pdb
import constants
from base_sqlite_manager import BaseSQLiteManager

class QueryDataInserter(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='queries'):
        super().__init__(db_name, table_name)
        self._create_table()

    def _create_table(self):
        sql = 'create table if not exists queries(' \
              'id integer primary key autoincrement, ' \
              'body text unique,' \
              'noun text,' \
              'cmp text,' \
              'verb text,' \
              'found_page integer,' \
              'unique(noun, cmp, verb)' \
              ');'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()

    def has_body(self, body):
        sql = 'select * from queries where exists(' \
              'select * from queries where body = "%s";' \
              ')' % body
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            return False
        if self.cur.fetchall():
            print('もうdbにあります')
            return True
        return False

    def insert(self, body, noun='', cmp='', verb='', found_page=True):
        if found_page:
            found_page_num = 1
        else:
            found_page_num = 0
        try:
            sql = 'insert into queries(body, noun, cmp, verb, found_page) ' \
                  'values("%s", "%s", "%s", "%s", %i);' \
                  % (body, noun, cmp, verb, found_page_num)
        except IndexError:
            print('%sの文のinsert失敗' % body)
            return False
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%sの入力完了！' % body)
        self.conn.commit()

if __name__ == '__main__':
    queries = constants.QUERIES_4
    with QueryDataInserter() as inserter:
        for query in queries:
            noun, cmp, verb = query.split('　')
            inserter.insert(body=query, noun=noun, cmp=cmp, verb=verb, found_page=True)
