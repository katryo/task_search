# -*- coding: utf-8 -*-
import constants
import os
import pickle
from path_mover import PathMover
import pdb


class PickleFileLoader(object):
    def load_ads_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_ADS_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        filenames = os.listdir()
        ads = []
        for filename in filenames:
            if filename == '.DS_Store':
                continue
            try:
                with open(filename, 'rb') as f:
                    ad = pickle.load(f)
                    ads.append(ad)
            except IsADirectoryError:
                pdb.set_trace()
        pm.go_up()
        pm.go_up()
        return ads


    def load_simple_task_search_result_with_query(self, query):
        os.chdir(constants.SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME)
        with open('%s.pkl' % query, 'rb') as f:
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

    def load_fetched_pages_with_query(self, query):
        path = os.path.join(constants.FETCHED_PAGES_DIR_NAME, query)
        os.chdir(path)
        pages = []
        for i in range(constants.NUM_OF_FETCHED_PAGES):
            with open('%s_%i.pkl' % (query, i), 'rb') as f:
                page = pickle.load(f)
                pages.append(page)
        os.chdir('../..')
        return pages

    def load_all_fetched_pages(self):
        os.chdir(constants.FETCHED_PAGES_DIR_NAME)
        pages = []
        for query in constants.QUERIES:
            os.chdir(query)
            for i in range(constants.NUM_OF_FETCHED_PAGES):
                with open('%s_%s.pkl' % (query, str(i)), 'rb') as f:
                    page = pickle.load(f)
                    if not hasattr(page, 'query'):
                        page.query = query
                    page.set_text_from_html_body()
                    pages.append(page)
            os.chdir('..')
        os.chdir('..')  # トップディレクトリに戻る
        return pages

    def load_entailment_dictionaries(self):
        os.chdir(constants.ENTAILMENT_DICTIONARIES_DIR_NAME)
        dictionaries = dict()
        for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
            for entailment_type in constants.ENTAILMENT_DICTIONARY_TYPES:
                with open('%s_%s.pkl' % (filename, entailment_type), 'rb') as f:
                    d = pickle.load(f)
                    dictionaries[filename + '_' + entailment_type] = d
        os.chdir('..')
        return dictionaries
