# -*- coding: utf-8 -*-
import pickle
import pdb


class PickleFileLoader(object):
    def load_file(self, filename):
        with open(filename, 'rb') as f:
            print('%sをロードします' % filename)
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

