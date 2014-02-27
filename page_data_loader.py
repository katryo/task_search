# -*- coding: utf-8 -*-
import sqlite3
import pdb
from base_sqlite_manager import BaseSQLiteManager

class PageDataLoader(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='pages'):
        super().__init__(db_name, table_name)

    def body_with_id(self, page_id):
        sql = 'select body from pages where id = %i;' % page_id
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        body = self.cur.fetchone()
        if not body:
            raise EOFError
        return body[0]

    def rank_with_query_url(self, query, url):
        sql = 'select rank from pages where query = "%s" and url = "%s";' % (query, url)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        rank = self.cur.fetchone()
        if not rank:
            pdb.set_trace()
            raise EOFError
        return rank[0]

    def page_ids_with_query(self, query):
        sql = 'select id from pages where query = "%s";' % query
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        ids = self.cur.fetchall()
        return [page_id[0] for page_id in ids]

    def pagedata_with_id(self, page_id):
        sql = 'select url, query, snippet, rank from pages where id = %i' % page_id
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        data = self.cur.fetchall()
        return data[0]

    def sentences_with_id(self, page_id):
        sql = 'select body from sentences where page_id = %i order by sequence;' % page_id
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
            raise EOFError
        data = self.cur.fetchall()
        return [item[0] for item in data]
