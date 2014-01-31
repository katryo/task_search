# -*- coding: utf-8 -*-
import constants
import pickle
import pdb
import os
from path_mover import PathMover
from pickle_file_saver import PickleFileSaver


class PickleFileSaverForEx(PickleFileSaver):
    def save_answerer_with_query(self, answerer, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.ANSWERER_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        with open('%s_answerer_first.pkl' % query, 'wb') as f:
            pickle.dump(answerer, f)
            print('%s_answerer_first.pklの保存完了！' % query)
        pm.go_up()
        pm.go_up()

    def can_find_graph_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.GRAPH_DIR_NAME)
        pm.go_or_create_and_go_to('first')
        pm.go_or_create_and_go_to(query)
        if os.path.exists(query + '_graph_first.pkl'):
            pm.go_up()
            pm.go_up()
            return True
        pm.go_up()
        pm.go_up()
        pm.go_up()
        return False

    def save_graph_with_query(self, obj, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.GRAPH_DIR_NAME)
        pm.go_or_create_and_go_to('first')
        pm.go_or_create_and_go_to(query)
        with open('%s_graph_first.pkl' % query, 'wb') as f:
            pickle.dump(obj, f)
            print('%s_graph_first.pklの保存完了！' % query)
        pm.go_up()
        pm.go_up()
        pm.go_up()
