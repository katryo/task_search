# -*- coding: utf-8 -*-
import constants
import pdb
from bing_searcher import BingSearcher
from pickle_file_saver_for_original import PickleFileSaverForOriginal

if __name__ == '__main__':
    queries = constants.QUERIES_1
    for query in queries:
        bs = BingSearcher(query)
        pages = bs.result_pages(page_num=1000)  # len(pages)が1000ないこともある
        saver = PickleFileSaverForOriginal()
        saver.save_pages_with_query(pages=pages, query=query)

