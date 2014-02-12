#coding: utf-8
from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pickle
import pdb


class PickleFileLoaderForAds(PickleFileLoader):
    def load_queries(self):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.QUERIES_DIR_NAME)
        filenames = os.listdir()
        queries = []
        for filename in filenames:
            if filename == '.DS_Store':
                continue
            try:
                with open(filename, 'rb') as f:
                    query = pickle.load(f)
                    queries.append(query)
            except IsADirectoryError:
                pdb.set_trace()
        pm.go_up()
        return queries

    def load_expanded_queries_with_query(self, query):
        expanded_queries = []
        filepath = os.path.join(constants.QUERIES_DIR_NAME, query + '.pkl')
        with open(filepath, 'rb') as f:
            expanded_query = pickle.load(f)
            expanded_queries.append(expanded_query)
        return expanded_queries


    def load_queries_with_original_query(self, original_query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.QUERIES_DIR_NAME)
        filenames = os.listdir()
        queries = []
        for filename in filenames:
            if filename == '.DS_Store':
                continue
            try:
                with open(filename, 'rb') as f:
                    query = pickle.load(f)
                    queries.append(query)
            except IsADirectoryError:
                pdb.set_trace()
        pm.go_up()
        return queries

    def load_ads_with_query(self, query):
        ads = []
        q_dirpath = os.path.join(constants.FETCHED_ADS_DIR_NAME, query)
        for dirpath, dirnames, filenames in os.walk(q_dirpath):
            for filename in filenames:
                if filename == '.DS_Store':
                    continue
                try:
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, 'rb') as f:
                        ad = pickle.load(f)
                        ads.append(ad)
                except IsADirectoryError:
                    pdb.set_trace()
        return ads

