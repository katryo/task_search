# -*- coding: utf-8 -*-
from pickle_file_loader_for_ads import PickleFileLoaderForAds
from pickle_file_saver_for_ads import PickleFileSaverForAds
import pdb
import constants

if __name__ == '__main__':
    pfl = PickleFileLoaderForAds()
    queries = ['野球　が　上手くなる',
               'ビリヤード　が　上手くなる',
               'サッカー　が　上手くなる',
               'ハンドボール　が　上手くなる']
    for query in queries:
        expanded_queries = pfl.load_expanded_queries_with_query(query)
        pfs = PickleFileSaverForAds()
        for expanded_query in expanded_queries:
            # query.body => '部屋　借りる', #query.expansion_words => ['家賃', '比較']
            print('%sをsearchします！' % expanded_query.body)
            pages = expanded_query.search_with_expansion_words()
            pfs.save_pages_with_query(pages_dict=pages,
                                      original_query=expanded_query.body)
            print('%sで検索して、その結果を保存しました！' % expanded_query.expansion_words)