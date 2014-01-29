# -*- coding: utf-8 -*-
import constants
import pickle
import pdb
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

