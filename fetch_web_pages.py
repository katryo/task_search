# -*- coding: utf-8 -*-
import constants
from bing_searcher import BingSearcher
from pickle_file_saver import PickleFileSaver

if __name__ == '__main__':
    bs = BingSearcher(constants.QUERY)
    pages = bs.result_pages()
    saver = PickleFileSaver()
    saver.save_pages_with_dir_name(pages=pages, dir_name=constants.QUERY)
    #pages = utils.search_web_pages(query)
    #utils.save_pages_with_dir_name(pages, query)
    """
    pm = PatternMatcher(constants.FINAL_QUERY)
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
    if not os.path.exists(constants.FINAL_QUERY):
        os.mkdir(constants.FINAL_QUERY)
    os.chdir(constants.FINAL_QUERY)
    pages = pm.bing_search()
    for i, page in enumerate(pages):
        with open('%s_%i.pkl' % (constants.FINAL_QUERY, i), 'wb') as f:
            pickle.dump(page, f)
    """