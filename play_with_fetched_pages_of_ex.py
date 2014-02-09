# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery

if __name__ == '__main__':
    loader = PickleFileLoaderForExpandedQuery()
    pages = loader.load_pages_with_task_with_query('犬　育てる')
    pdb.set_trace()