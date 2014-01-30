# -*- coding: utf-8 -*-
from pickle_file_loader_for_ads import PickleFileLoaderForAds
from pickle_file_saver_for_ads import PickleFileSaverForAds
import pdb
import constants

# 1000件以上検索するようにする？？？

if __name__ == '__main__':
    pfl = PickleFileLoaderForAds()
    queries = pfl.load_queries()
    pfs = PickleFileSaverForAds()
    for query in queries:
        # query.body => '部屋　借りる', #query.expansion_words => ['家賃', '比較']
        if pfs.can_find_pages_with_query_dir(query.body, query.expansion_words):
            print('%sはもうあります' % query.body)
            continue
        pages = query.search_with_expansion_words()
        pfs.save_pages_with_query(pages_dict=pages,
                                  original_query=query.body)
        print('%sで検索して、その結果を保存しました！' % query.expansion_words)