# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver

# 1000件以上検索するようにする？？？

if __name__ == '__main__':
    pfl = PickleFileLoader()
    queries = pfl.load_queries()

    pfs = PickleFileSaver()
    for query in queries:
        pages = query.search_with_expansion_words()
        pfs.save_pages_with_query_expansion(pages=pages, query_obj=query)