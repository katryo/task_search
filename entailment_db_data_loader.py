import pdb
from base_sqlite_manager import BaseSQLiteManager
from sqlite_data_loadable import SQLiteDataLoadable

class EntailmentDBDataLoader(BaseSQLiteManager, SQLiteDataLoadable):
    def __init__(self, table_name='entailment_ntriv'):
        super().__init__(db_name='entailment.sqlite', table_name=table_name)

if __name__ == '__main__':
    el = EntailmentDBDataLoader()
    print(el.select_all_with_max_num())