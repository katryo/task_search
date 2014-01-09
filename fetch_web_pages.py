# -*- coding: utf-8 -*-
import constants
from bing_searcher import BingSearcher
from pickle_file_saver import PickleFileSaver

if __name__ == '__main__':
    bs = BingSearcher(constants.QUERY)
    pages = bs.result_pages()
    saver = PickleFileSaver()
    saver.save_pages_with_dir_name(pages=pages, dir_name=constants.QUERY)

