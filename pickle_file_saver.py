# -*- coding: utf-8 -*-
import constants
import os
import pickle
import pdb
from path_mover import PathMover


class PickleFileSaver(object):
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

    def save_simple_task_search_result_with_query(self, results_dic, query):
        if not os.path.exists(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME):
            os.mkdir(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME)
        os.chdir(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME)
        with open('%s.pkl' % query, 'wb') as f:
            pickle.dump(obj=results_dic, file=f)
        os.chdir('..')

    def save_pages_with_query(self, pages, query):
        os.chdir(constants.FETCHED_PAGES_DIR_NAME)
        os.chdir(query)
        for i in range(constants.NUM_OF_FETCHED_PAGES):
            with open('%s_%i.pkl' % (query, i), 'wb') as f:
                try:
                    pickle.dump(pages[i], f)
                except TypeError:
                    pdb.set_trace()
                print('%s_%i.pklの保存完了!' % (query, i))
        os.chdir('..')

    # constants.QUERIES依存なのでちょっと危険。
    def save_all_pages(self, pages):
        # fetched_pagesのひとつ上のディレクトリからfetched_pagesに降りる
        os.chdir(constants.FETCHED_PAGES_DIR_NAME)
        for query in constants.QUERIES:
            os.chdir(query)
            for i in range(constants.NUM_OF_FETCHED_PAGES):
                num_of_page = constants.QUERIES.index(query) * 50 + i
                with open('%s_%i.pkl' % (query, i), 'wb') as f:
                    pickle.dump(pages[num_of_page], f)
                    print('%s_%i.pklの保存完了!' % (query, i))
            os.chdir('..')
