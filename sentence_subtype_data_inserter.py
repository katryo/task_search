# -*- coding: utf-8 -*-
import sqlite3
import pdb
import constants
from base_sqlite_manager import BaseSQLiteManager
from subtype_data_loader import SubtypeDataLoader
from sentence_data_loader import SentenceDataLoader

class SentenceSubtypeDataInserter(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='sentence_subtype'):
        super().__init__(db_name, table_name)
        self._create_table()

    def _create_table(self):
        sql = 'create table if not exists sentence_subtype(' \
              'id integer primary key autoincrement, ' \
              'sentence_id integer,' \
              'subtype_id integer,' \
              'unique(sentence_id, subtype_id));'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()

    def has_sentence_subtype(self, sentence_id, subtype_id):
        sql = 'select id from sentence_subtype ' \
              'where sentence_id = %i and subtype_id = %i' % (sentence_id, subtype_id)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        result = self.cur.fetchone()
        if result:
            print('もう%iはdbにあります' % result[0])
            return True
        print('dbにないです')
        return False

    def insert(self, sentence_id, subtype_id):
        try:
            sql = 'insert into sentence_subtype(sentence_id, subtype_id) ' \
                  'values(%i, %i);' \
                  % (sentence_id, subtype_id)
        except IndexError:
            print('%iの文のinsert失敗' % sentence_id)
            return False
        except TypeError:
            pdb.set_trace()
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%iの入力完了！' % sentence_id)
        try:
            self.conn.commit()
        except sqlite3.OperationalError:
            print('たぶんロックされてます')

if __name__ == '__main__':
    queries = constants.QUERIES_4
    with SentenceDataLoader() as sentence_loader:
        for query in queries:
            supertype_noun = query.split('　')[0]
            with SubtypeDataLoader() as subtype_loader:
                try:
                    subtype_nouns = subtype_loader.bodies_with_supertype_noun(supertype_noun=supertype_noun)
                except EOFError:
                    continue
                sentence_ids = sentence_loader.ids_with_query(query)
                for sentence_id_tuple in sentence_ids:
                    sentence_id = sentence_id_tuple[0]
                    for subtype_noun in subtype_nouns:
                        if sentence_loader.has_subtype_with_id_and_subtype_noun(sentence_id=sentence_id,
                                                                       subtype_noun=subtype_noun[0]):
                            subtype_id = subtype_loader.id_with_body(subtype_noun)
                            with SentenceSubtypeDataInserter() as inserter:
                                if inserter.has_sentence_subtype(sentence_id=sentence_id, subtype_id=subtype_id):
                                    continue
                                inserter.insert(sentence_id=sentence_id, subtype_id=subtype_id)