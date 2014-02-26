#coding: utf-8
from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pickle
import pdb


class PickleFileLoaderForOriginal(PickleFileLoader):
    def load_fetched_pages_with_query(self, query):
        dirpath = os.path.join(constants.FETCHED_PAGES_DIR_NAME, query)
        pages = []
        for i in range(1000):
            filename = query + '_%i.pkl' % i
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'rb') as f:
                    page = pickle.load(f)
                    page.rank = i
                    pages.append(page)
            except (EOFError, FileNotFoundError):  #1000個ないとき
                print('%iページしかないです' % i)
                break
        return pages

    def load_graph_with_query(self, query):
        path = os.path.join(constants.GRAPH_DIR_NAME, query, query+'_graph_zero.pkl')
        graph = self.load_file(path)
        return graph

