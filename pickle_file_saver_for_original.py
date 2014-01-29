# -*- coding: utf-8 -*-
import constants
import os
import pickle
import pdb
from path_mover import PathMover
from pickle_file_saver import PickleFileSaver


class PickleFileSaverForOriginal(PickleFileSaver):
    def save_pages_with_query(self, pages, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_O_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        for i in range(constants.NUM_OF_FETCHED_PAGES):
            with open('%s_%i.pkl' % (query, i), 'wb') as f:
                try:
                    pickle.dump(pages[i], f)
                    print('%s_%i.pklの保存完了!' % (query, i))
                except (TypeError, IndexError):
                    print('%sは%i個までしかありません！' % (query, i))
                    break
        pm.go_up()
        pm.go_up()

