# -*- coding: utf-8 -*-
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from pickle_file_saver_for_original import PickleFileSaverForOriginal
import constants

if __name__ == '__main__':
    queries = constants.QUERIES_1
    for query in queries:
        query = '部屋　掃除する'
        pfl = PickleFileLoaderForOriginal()
        pages = pfl.load_fetched_pages_with_query(query)
        for i, page in enumerate(pages):
            page.set_tasks_from_sentences()
            print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))

        pfs = PickleFileSaverForOriginal()
        pfs.save_pages_with_query(pages=pages, query=query)
