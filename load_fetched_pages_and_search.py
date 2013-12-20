import constants
import os
from pattern_matcher import PatternMatcher
import pdb
import pickle
import utils

if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    keywords = set()
    for page in pages:
        try:
            keyword = page.noun_before_query(page.snippet, constants.ACTION_WORD_IN_QUERY)
        except (ValueError, IndexError):
            continue
        if keyword:
            keywords.add(keyword)
    print(keywords)

    # 〜〜を使う、の〜〜も最終結果に入れる
    results_dic = {}
    for keyword in keywords:
        results_dic[keyword] = set()

    for keyword in keywords:
        pm = PatternMatcher(constants.QUERY + ' "' + constants.SO_CALLED + keyword + '"')
        keyword_pages = pm.bing_search()
        for page in keyword_pages:
            try:
                result = page.noun_before_query(page.snippet, constants.SO_CALLED + keyword)
            except (ValueError, IndexError):
                continue
            if result:
                # results_dic[keyword] => set()からset(['アレロック', 'アルガード'])
                results_dic[keyword].add(result)

    with open(constants.PICKLE_RESULT_DICT_NAME, 'wb') as f:
        pickle.dump(results_dic, f)

    pdb.set_trace()
