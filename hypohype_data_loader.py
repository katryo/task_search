# -*- coding: utf-8 -*-
import sqlite3
import constants
import pdb
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable


class HypoHypeDBDataLoader(BaseSQLiteManager, SQLiteDataLoadable):
    def select_hypes_with_hypo(self, hypo):
        sql = 'select hypernym, score from all_hyponymy where hyponym = "%s" limit 100' % hypo
        self.cur.execute(sql)
        print('%sを実行！' % sql)
        results = [tpl[0] for tpl in self.cur.fetchall() if tpl[1] > 0]
        return results

    def hypes_except_for_blockwords(self, hypo):
        hypes = self.select_hypes_with_hypo(hypo)
        for hype in hypes:
            for stopword in constants.STOPWORDS_OF_HYPOHYPE:
                if stopword in hype:
                    hypes.remove(hype)
                    break  # もうhypoはhypesにないからstopwordsから探す必要なし
        return hypes

    def select_hypos_with_hype(self, hype):
        sql = 'select hyponym, score from  all_hyponymy where hypernym = "%s" limit 100' % hype
        self.cur.execute(sql)
        results = [tpl[0] for tpl in self.cur.fetchall() if tpl[1] > 0]
        return results

    def has(self, hypernym, hyponym):
        sql = 'select * from  all_hyponymy where exists(' \
              'select * from  all_hyponymy where hypernym = "%s" and hyponym = "%s"' \
              ')' % (hypernym, hyponym)
        self.cur.execute(sql)
        if self.cur.fetchall():
            return True
        return False

    def insert(self, cs_text):
        items = cs_text.split(',')
        if self.has(items[0], items[1]):
            print('%sはすでに存在しているのでスキップしました' % cs_text)
            return False
        try:
            sql = 'insert into all_hyponymy(hypernym, hyponym, score, type) values("%s", "%s", %s, "%s")' \
                  % (items[0], items[1], items[2], items[3])
        except IndexError:
            print('%sのinsert失敗' % cs_text)
            return False
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        print('%sの入力完了！' % cs_text)
        self.conn.commit()

    def show_all(self):
        sql = 'select * from %s' % self.table_name
        self.cur.execute(sql)
        for row in self.cur:
            print(row)

