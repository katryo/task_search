# -*- coding: utf-8 -*-
import sqlite3
import pdb
import constants
from base_sqlite_manager import BaseSQLiteManager
from hypohype_data_loader import HypoHypeDBDataLoader

class SubtypeDataInserter(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='subtype_nouns'):
        super().__init__(db_name, table_name)
        self._create_table()

    def _create_table(self):
        sql = 'create table if not exists subtype_nouns(' \
              'id integer primary key autoincrement, ' \
              'body text, ' \
              'supertype_noun text ' \
              ');'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()

    def has_body(self, body):
        sql = 'select * from subtype_nouns where exists(' \
              'select * from subtype_nouns where body = "%s";' \
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

    def insert(self, body, supertype_noun):
        try:
            sql = 'insert into subtype_nouns(body, supertype_noun) ' \
                  'values("%s", "%s");' \
                  % (body, supertype_noun)
        except IndexError:
            print('%sの文のinsert失敗' % body)
            return False
        try:
            self.cur.execute(sql)
        except (sqlite3.OperationalError, sqlite3.IntegrityError):
            pdb.set_trace()
        print('%sの入力完了！' % body)
        self.conn.commit()

if __name__ == '__main__':
    queries = constants.QUERIES_4
    with SubtypeDataInserter() as inserter:
        with HypoHypeDBDataLoader() as loader:
            for query in queries:
                hype = query.split('　')[0]
                hypos = loader.select_hypos_with_hype(hype)
                for hypo in hypos:
                    inserter.insert(body=hypo, supertype_noun=hype)
