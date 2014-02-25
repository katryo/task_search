# -*- coding: utf-8 -*-
import sqlite3
import pdb
from base_sqlite_manager import BaseSQLiteManager

class SentenceDataLoader(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='sentences'):
        super().__init__(db_name, table_name)

    def ids_with_query(self, query):
        sql = 'select sentences.id from sentences, pages where pages.query = "%s" and sentences.page_id = pages.id;' % query
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        ids = self.cur.fetchall()
        return ids  # [(1, ), (2, ), ...]

    def body_with_id(self, sentence_id):
        sql = 'select body from sentences where id = %i;' % sentence_id
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        body = self.cur.fetchone()
        if not body:
            raise EOFError
        return body[0]

    def has_subtype_with_id_and_subtype_noun(self, sentence_id, subtype_noun):
        body = self.body_with_id(sentence_id)
        if subtype_noun in body:
            return True
        return False

