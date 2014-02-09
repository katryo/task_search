# -*- coding: utf-8 -*-
import pdb
import constants
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery

if __name__ == '__main__':
    loader = PickleFileLoaderForExpandedQuery()
    pages = loader.load_fetched_pages_with_query('部屋　掃除する')
    for page in pages:
        indexes = page.subtype_indexes()
        print(indexes)
    pdb.set_trace()