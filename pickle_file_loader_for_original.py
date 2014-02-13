#coding: utf-8
from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pickle
import pdb


class PickleFileLoaderForOriginal(PickleFileLoader):
    def load_fetched_pages_with_query(self, query):
        path = os.path.join(constants.FETCHED_PAGES_O_DIR_NAME, query)
        pages = []
        for dirpath, dirname, filenames in os.walk(path):
            for filename in filenames:
                if not filename == '.DS_Store':
                    try:
                        filepath = os.path.join(dirpath, filename)
                        with open(filepath, 'rb') as f:
                            page = pickle.load(f)
                            pages.append(page)
                    except EOFError:  #1000個ないとき
                        break
        return pages

    def load_graph_with_query(self, query):
        path = os.path.join(constants.FETCHED_PAGES_O_DIR_NAME, query+'_graph_zero.pkl')
        graph = self.load_file(path)
        return graph

