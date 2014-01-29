# -*- coding: utf-8 -*-
import constants
import pickle
import pdb
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
