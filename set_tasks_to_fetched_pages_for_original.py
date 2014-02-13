# -*- coding: utf-8 -*-
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from pickle_file_saver_for_original import PickleFileSaverForOriginal
import constants

if __name__ == '__main__':
    queries = constants.QUERIES_4
    for query in queries:
        pfl = PickleFileLoaderForOriginal()
        pages = pfl.load_fetched_pages_with_query(query)
        for i, page in enumerate(pages):
            if hasattr(page, 'tasks'):
                if page.tasks:
                    print('すでにtasksがあります')
                    continue
            page.set_tasks_from_sentences()
            print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))

        pfs = PickleFileSaverForOriginal()
        pfs.save_pages_with_query(pages=pages, query=query)
