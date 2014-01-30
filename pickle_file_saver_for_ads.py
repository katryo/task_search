# -*- coding: utf-8 -*-
import constants
import pickle
import pdb
import os
from path_mover import PathMover
from pickle_file_saver import PickleFileSaver


class PickleFileSaverForAds(PickleFileSaver):
    def save_query(self, query_obj):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.QUERIES_DIR_NAME)
        with open('%s.pkl' % query_obj.body, 'wb') as f:
            pickle.dump(obj=query_obj, file=f)
            print('%sの保存完了' % query_obj.body)
        pm.go_up()

    def save_ads_with_query(self, ads, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_ADS_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        for i, ad in enumerate(ads):
            with open('%s_%i.pkl' % (ad.title, i), 'wb') as f:
                pickle.dump(obj=ad, file=f)
                print('%sの保存完了' % ad.title)
        pm.go_up()
        pm.go_up()

    def can_find_pages_with_query_dir(self, query, words):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        for word in words:
            if os.path.exists('%s　%s' % (query, word)):  # 拡張クエリのディレクトリ発見！
                pm.go_or_create_and_go_to(word)
                if os.path.exists('%s　%s_1.pkl' % (query, word)):
                    pm.go_up()
                    pm.go_up()
                    pm.go_up()
                    print('すでにある')
                    return True
                pm.go_up()
                pm.go_up()
                pm.go_up()
                print('ない1')
                return False
            pm.go_up()
            pm.go_up()
            print('ない2')
            return False

    def save_pages_with_query(self, pages_dict, original_query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
        pm.go_or_create_and_go_to(original_query)
        for expanded_query in pages_dict:
            pm.go_or_create_and_go_to(expanded_query)
            for i in range(constants.NUM_OF_FETCHED_PAGES):
                with open('%s_%i.pkl' % (expanded_query, i), 'wb') as f:
                    try:
                        pickle.dump(pages_dict[expanded_query][i], f)
                        print('%s_%i.pklの保存完了!' % (expanded_query, i))
                    except (TypeError, IndexError):
                        print('%sは%i個までしかありません！' % (expanded_query, i))
                        break
            pm.go_up()
        pm.go_up()
        pm.go_up()
