# -*- coding: utf-8 -*-
import utils
import pdb


if __name__ == '__main__':
    query = 'ゴールデンタイム 骨折'
    utils.search_and_save_web_pages(query)
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