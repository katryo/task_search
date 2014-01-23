# -*- coding: utf-8 -*-
import constants
from bing_searcher import BingSearcher
from pickle_file_saver import PickleFileSaver

if __name__ == '__main__':
    query = '部屋　掃除する'
    bs = BingSearcher(query)
    pages = bs.result_pages()
    saver = PickleFileSaver()
    saver.save_pages_with_query(pages=pages, query=query)

