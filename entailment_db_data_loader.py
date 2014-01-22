import pdb
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class EntailmentDBDataLoader(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, table_name='entailment_ntriv'):
        super().__init__(db_name='entailment.sqlite', table_name=table_name)

    def entailed_with_entailing(self, entailing):
        sql = 'select entailed from %s where entailing = "%s"' % (self.table_name, entailing)
        self.cur.execute(sql)
        tuple_in_list = self.cur.fetchall()
        if tuple_in_list:
            results = tuple_in_list[0]
            return results
        return []

    def entailing_with_entailed(self, entailed):
        sql = 'select entailing from %s where entailed = "%s"' % (self.table_name, entailed)
        self.cur.execute(sql)
        tuple_in_list = self.cur.fetchall()
        if tuple_in_list:
            results = tuple_in_list[0]
            return results
        return []

if __name__ == '__main__':
    el = EntailmentDBDataLoader()
    print(el.select_all_with_max_num())