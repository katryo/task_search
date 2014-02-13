# -*- coding: utf-8 -*-
import constants
import os
import pickle
import pdb
from path_mover import PathMover
from pickle_file_saver import PickleFileSaver


class PickleFileSaverForOriginal(PickleFileSaver):
    def save_pages_with_query(self, pages, query):
        dirpath = os.path.join(constants.FETCHED_PAGES_O_DIR_NAME, query)
        for d_dirpath, dirnames, filenames in os.walk(dirpath):
            for i, page in enumerate(pages):
                filename = os.path.join(d_dirpath, '%s_%i.pkl' % (query, i))
                with open(filename, 'wb') as f:
                    try:
                        pickle.dump(page, f)
                        print('%s_%i.pklの保存完了!' % (query, i))
                    except (TypeError, IndexError):
                        print('%sは%i個までしかありません！' % (query, i))
                        break

    def save_graph_with_query(self, obj, query):
        filepath = os.path.join(constants.GRAPH_DIR_NAME, query + '_graph_zero.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
            print('%s_graph_zero.pklの保存完了！' % query)

    def can_find_page_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_O_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        if os.path.exists('%s_10.pkl' % query):
            pm.go_up()
            pm.go_up()
            return True
        pm.go_up()
        pm.go_up()
        return False

    def can_find_graph_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.GRAPH_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        if os.path.exists(query + '_graph_zero.pkl'):
            pm.go_up()
            pm.go_up()
            return True
        pm.go_up()
        pm.go_up()
        return False

    def save_answerer_with_query(self, answerer, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.ANSWERER_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        with open('%s_answerer_zero.pkl' % query, 'wb') as f:
            pickle.dump(answerer, f)
            print('%s_answerer_zero.pklの保存完了！' % query)
        pm.go_up()
        pm.go_up()
