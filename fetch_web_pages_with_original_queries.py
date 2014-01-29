# -*- coding: utf-8 -*-
import constants
from bing_searcher import BingSearcher
from pickle_file_saver import PickleFileSaver

if __name__ == '__main__':
    queries = constants.QUERIES
    for query in queries:
        bs = BingSearcher(query)
        pages = bs.result_pages(page_num=1000)
        saver = PickleFileSaver()
        saver.save_pages_with_original_query(pages=pages, query=query)

