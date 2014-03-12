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

    def sentence_after_sentence_with_body_url(self, body, url):
        page_id, sentence_id = self._id_after_sentence_with_body_url(body, url)
        return self._sentences_after_sentence_with_id_page_id(sentence_id, page_id)



    def _id_after_sentence_with_body_url(self, body, url):
        sql = 'select pages.id, sentences.id from sentences, pages where sentences.body = "%s" and ' \
              'sentences.page_id = pages.id and pages.url = "%s" ;' % (body, url)
        try:
            print('%sを実行します！' % sql)
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            raise EOFError
        page_id, sentence_id = self.cur.fetchone()
        print('page_idは%iです' % page_id)
        return page_id, sentence_id

    def _sentences_after_sentence_with_id_page_id(self, sentence_id, page_id):
        sql = 'select body from sentences where id > %i and ' \
              'page_id = %i ;' % (sentence_id, page_id)
        try:
            print('%sを実行します！' % sql)
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        sentences_in_tuples = self.cur.fetchall()
        if not sentences_in_tuples:
            return []
        return [sentence[0] for sentence in sentences_in_tuples]

