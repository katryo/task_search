# -*- coding: utf-8 -*-
import constants
import pdb
from bing_searcher import BingSearcher
from pickle_file_saver_for_original import PickleFileSaverForOriginal

if __name__ == '__main__':
    queries = ['保育園　入園させる']
    saver = PickleFileSaverForOriginal()
    for query in queries:
        if saver.can_find_page_with_query(query):
            print('%sはもうあります' % query)
            continue
        bs = BingSearcher(query)
        pages = bs.result_pages(page_num=1000)  # len(pages)が1000ないこともある
        saver.save_pages_with_query(pages=pages, query=query)

