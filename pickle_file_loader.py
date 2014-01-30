# -*- coding: utf-8 -*-
import constants
import os
import pickle
from path_mover import PathMover
import pdb


class PickleFileLoader(object):
    def load_file(self, filename):
        with open(filename, 'rb') as f:
            try:
                obj = pickle.load(f)
            except EOFError:
                raise EOFError
        return obj

    def load_fetched_pages_with_query(self, query):
        #override me!
        pass

    def load_graph_with_query(self, query):
        #override me!
        pass

