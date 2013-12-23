import os
import constants
import pickle
from pattern_matcher import PatternMatcher


if __name__ == '__main__':
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