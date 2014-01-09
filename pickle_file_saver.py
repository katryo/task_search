# -*- coding: utf-8 -*-
import constants
import os
import pickle
import pdb


class PickleFileSaver(object):
    def save_simple_task_search_result(self, results_dic):
        if not os.path.exists(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME):
            os.mkdir(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME)
        os.chdir(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME)
        with open('%s.pkl' % constants.FINAL_QUERY, 'wb') as f:
            pickle.dump(obj=results_dic, file=f)
        os.chdir('..')

    def save_pages_with_dir_name(self, pages, dir_name):
        os.chdir(constants.FETCHED_PAGES_DIR_NAME)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        os.chdir(dir_name)
        for i in range(constants.NUM_OF_FETCHED_PAGES):
            with open('%s_%i.pkl' % (dir_name, i), 'wb') as f:
                try:
                    pickle.dump(pages[i], f)
                except TypeError:
                    pdb.set_trace()
                print('%s_%i.pklの保存完了!' % (dir_name, i))
        os.chdir('..')
