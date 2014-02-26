# -*- coding: utf-8 -*-
import sqlite3
import pdb
from base_sqlite_manager import BaseSQLiteManager
from task_data_selector import TaskDataSelector

class TaskSubtypeDataInserter(BaseSQLiteManager):
    def __init__(self, db_name='tasks.sqlite', table_name='task_subtype'):
        super().__init__(db_name, table_name)
        self._create_table()

    def _create_table(self):
        sql = 'create table if not exists task_subtype(' \
              'id integer primary key autoincrement, ' \
              'task_id integer, ' \
              'subtype_id integer, ' \
              'distance_from_subtype_to_task integer, ' \
              'unique(task_id, subtype_id, distance_from_subtype_to_task)' \
              ');'
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            pdb.set_trace()


    def has(self, task_id, subtype_id):
        sql = 'select * from  task_subtype where ' \
              'sentence_id = %i and subtype_id = %i;' % (task_id, subtype_id)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError:
            return False
        if self.cur.fetchall():
            return True
        return False

    def insert(self, task_id, subtype_id, distance_from_subtype_to_task):
        if self.has(task_id=task_id, subtype_id=subtype_id):
            print('%iのタスクはすでに存在しているのでスキップしました' % task_id)
            return False
        try:
            sql = 'insert into task_subtype(task_id, subtype_id, distance_from_subtype_to_task) ' \
                  'values(%i, %i, %i)' % (task_id, subtype_id, distance_from_subtype_to_task)
        except IndexError:
            print('%iのタスクのsubtype関係のinsert失敗' % task_id)
            return False
        try:
            self.cur.execute(sql)
            print('%iの入力完了！' % task_id)
        except sqlite3.OperationalError:
            pdb.set_trace()
        except sqlite3.IntegrityError:
            print('uniqueなはずなのでこのデータ入れないでおきますね')
        self.conn.commit()


if __name__ == '__main__':
    with TaskSubtypeDataInserter() as inserter:
        with TaskDataSelector() as task_selector:
            for task_id in range(20000):
                subtype_ids = task_selector.subtype_ids_with_task_id(task_id=task_id)  # taskが出現したページ内のsubtype_idたち
                if subtype_ids:
                    for subtype_id in subtype_ids:
                        # subtypeの出現したsentenceのsequenceを特定
                        subtype_sentence_sequence = task_selector.subtype_sentence_sequence(subtype_id=subtype_id)
                        # taskの出現したsentenceのsequenceを特定
                        task_sentence_sequence = task_selector.task_sentence_sequence(task_id=task_id)
                        distance = task_sentence_sequence - subtype_sentence_sequence
                        inserter.insert(task_id=task_id,
                                        subtype_id=subtype_id,
                                        distance_from_subtype_to_task=distance)
