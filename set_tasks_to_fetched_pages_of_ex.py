# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_saver_for_ex import PickleFileSaverForEx
import constants
import pdb


if __name__ == '__main__':
    pfl = PickleFileLoaderForExpandedQuery()
    pfs = PickleFileSaverForEx()

    original_queries = constants.QUERIES_4
    for query in original_queries:
        pages = pfl.load_fetched_pages_with_query(query)
        for i, page in enumerate(pages):
            if hasattr(page, 'tasks'):
                if page.tasks:
                    print('すでにtasksがあります')
                    continue
            page.set_tasks_from_sentences()
            print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))
            pfs.save_page_with_original_query(page=page, original_query=query, i=i)

