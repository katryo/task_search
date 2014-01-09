# -*- coding: utf-8 -*-
import sqlite3
import pdb


class SQLiteDataLoader(object):
    def __init__(self):
        self.conn = sqlite3.connect('hyponym_hypernym.sqlite')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def select_hypes_with_hypo(self, hypo):
        sql = 'select hypernym, score from all_hyponymy where hyponym = "%s"' % hypo
        self.cur.execute(sql)
        results = [tpl[0] for tpl in self.cur.fetchall() if tpl[1] > 0]
        return results

    def select_hypos_with_hype(self, hype):
        sql = 'select hyponym, score from  all_hyponymy where hypernym = "%s"' % hype
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
        sql = 'select * from all_hyponymy'
        self.cur.execute(sql)
        for row in self.cur:
            print(row)

