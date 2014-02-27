# -*- coding: utf-8 -*-
import sqlite3
import pdb
import constants
from base_sqlite_manager import BaseSQLiteManager
from subtype_data_loader import SubtypeDataLoader
from sentence_data_loader import SentenceDataLoader

class SentenceDataInserter(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='sentences'):
        super().__init__(db_name, table_name)
        self._create_table()

    def _create_table(self):
        sql = 'create table if not exists sentences(' \
              'id integer primary key autoincrement, ' \
              'page_id integer,' \
              'body text,' \
              'sequence integer,' \
              'unique(page_id, sequence));'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()


    def has_body(self, page_id, sequence):
        sql = 'select * from sentences where exists(' \
              'select * from sentences where page_id = %i and sequence = %i;' \
              ')' % (page_id, sequence)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            return False
        if self.cur.fetchall():
            print('もうdbにあります')
            return True
        return False

    def insert(self, body, page_id, sequence):
        try:
            sql = 'insert into sentences(body, page_id, sequence) ' \
                  'values("%s", %i, %i);' \
                  % (body, page_id, sequence)
        except IndexError:
            print('%sの文のinsert失敗' % body)
            return False
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%sの入力完了！' % body)
        self.conn.commit()

    def update_has_subtype(self, sentence_id, has_subtype):
        if has_subtype:
            has_subtype_num = 1
        else:
            has_subtype_num = 0
        sql = 'update sentences set has_subtype=%i;' % has_subtype_num
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%sの入力完了！' % str(sentence_id))
        self.conn.commit()

if __name__ == '__main__':
    queries = constants.QUERIES_4
    with SentenceDataLoader() as loader:
        for query in queries:
            supertype_noun = query.split('　')[0]
            with SubtypeDataLoader() as subtype_loader:
                subtype_nouns = subtype_loader.body_with_supertype_noun(supertype_noun=supertype_noun)
                ids = loader.ids_with_query(query)
                for sentence_id in ids:
                    for subtype_noun in subtype_nouns:
                        if loader.has_subtype_with_id_and_subtype_noun(sentence_id=sentence_id,
                                                                       subtype_noun=supertype_noun):
                            has_subtype = True
                        with SentenceDataInserter() as inserter:
                            inserter.update_has_subtype(sentence_id=sentence_id, has_subtype=has_subtype)
