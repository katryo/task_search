# -*- coding: utf-8 -*-
import constants
import pickle
import pdb
import os
from path_mover import PathMover
from pickle_file_saver import PickleFileSaver


class PickleFileSaverForEx(PickleFileSaver):
    def save_page_with_original_query(self, page, original_query, i):
        original_query_dirpath = os.path.join(constants.FETCHED_PAGES_WITH_TASK_FOR_EX_DIR_NAME, original_query)
        if not os.path.exists(original_query_dirpath):
            os.mkdir(original_query_dirpath)
        expanded_query_dirpath = os.path.join(constants.FETCHED_PAGES_WITH_TASK_FOR_EX_DIR_NAME, original_query, page.query)
        if not os.path.exists(expanded_query_dirpath):
            os.mkdir(expanded_query_dirpath)
        for dirpath, dirnames, filenames in os.walk(expanded_query_dirpath):
            if page.title in filenames:
                return  #すでに保存してある
            filename = '%s_%i.pkl' % (page.query, i)
            filepath = os.path.join(dirpath, filename)
            self.save_file(obj=page, filename=filepath)
            print('%sの%i番目のセーブに成功しました！' % (page.query, i))

    def save_answerer_with_query(self, answerer, query):
        path = os.path.join(constants.ANSWERER_DIR_NAME, query)
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename == '%s_answerer_first.pkl' % query:
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, 'wb') as f:
                        pickle.dump(answerer, f)
                        print('%s_answerer_first.pklの保存完了！' % query)

    def can_find_graph_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.GRAPH_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        if os.path.exists(query + '_graph_first.pkl'):
            pm.go_up()
            pm.go_up()
            return True
        pm.go_up()
        pm.go_up()
        return False

    def save_graph_with_query(self, obj, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.GRAPH_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        with open('%s_graph_first.pkl' % query, 'wb') as f:
            pickle.dump(obj, f)
            print('%s_graph_first.pklの保存完了！' % query)
        pm.go_up()
        pm.go_up()
