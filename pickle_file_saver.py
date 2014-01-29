# -*- coding: utf-8 -*-
import pickle
import pdb


class PickleFileSaver(object):
    def save_file(self, obj, filename):
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)
        return obj

    def save_graph_with_query(self, obj, query):
        #override me!
        pass

    def save_pages_with_query(self, pages, query):
        #override me!
        pass