# -*- coding: utf-8 -*-
import pdb

class SQLiteDataLoadable(object):
    def select_all_with_max_num(self, num=5):
        sql = 'select * from %s limit %i' % (self.table_name, num)
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results
