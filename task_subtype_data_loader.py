# -*- coding: utf-8 -*-
import pdb
import numpy
import sqlite3
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class TaskSubtypeDataLoader(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, db_name='tasks.sqlite', table_name='task_subtype'):
        super().__init__(db_name, table_name)

    def distance_from_subtype_with_task_id(self, task_id):
        sql = 'select subtype_nouns.body, task_subtype.distance_from_subtype_to_task ' \
              'from task_subtype, subtype_nouns ' \
              'where task_subtype.subtype_id = subtype_nouns.id ' \
              'and task_subtype.task_id = %i;' % task_id
        try:
            self.cur.execute(sql)
            print('%sを実行！' % sql)
        except sqlite3.OperationalError:
            pdb.set_trace()
        results = self.cur.fetchall()
        return results

if __name__ == '__main__':
    with TaskSubtypeDataLoader() as loader:
        for i in range(20000):
            loader.distance_from_subtype_with_task_id(i+1)

