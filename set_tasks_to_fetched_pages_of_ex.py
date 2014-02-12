# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_saver_for_ex import PickleFileSaverForEx
from path_mover import PathMover
import constants
import pdb
import os


if __name__ == '__main__':
    pfl = PickleFileLoaderForExpandedQuery()
    pfs = PickleFileSaverForEx()
    pm = PathMover()

    original_queries = constants.QUERIES_4
    for query in original_queries:
        pages = pfl.load_fetched_pages_with_query(query)
        pdb.set_trace()
        for i, page in enumerate(pages):
            if hasattr(page, 'tasks'):
                if page.tasks:
                    print('すでにtasksがあります')
                    # が、無視。上書き。continue
            page.set_tasks_from_sentences()
            print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))
            pfs.save_page_with_original_query(page=page, original_query=query, i=i)

