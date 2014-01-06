# -*- coding: utf-8 -*-
import constants
import os
import pickle


class PickleFileLoader(object):
    def load_simple_task_search_result(self):
        os.chdir(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME)
        with open('%s.pkl' % constants.FINAL_QUERY, 'rb') as f:
            results_dic = pickle.load(f)
        os.chdir('..')
        return results_dic

    def load_object_term_dictionary(self):
        os.chdir(constants.OBJECT_TERM_DICTIONARY_DIR_NAME)
        with open(constants.OBJECT_TERM_DICTIONARY_PICKLE_FILENAME, 'rb') as f:
            object_term_dictionary = pickle.load(f)
            print('%sのロード完了!' % constants.OBJECT_TERM_DICTIONARY_PICKLE_FILENAME)
        os.chdir('..')
        return object_term_dictionary
