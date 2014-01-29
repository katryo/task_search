#coding: utf-8
from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pickle
import pdb


class PickleFileLoaderForEx(PickleFileLoader):
    def load_queries(self):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.QUERIES_DIR_NAME)
        filenames = os.listdir()
        queries = []
        for filename in filenames:
            if filename == '.DS_Store':
                continue
            if not filename[:-4] in constants.QUERIES:
                continue  # 以前使って、消した花粉症対策のようなクエリかも
            try:
                with open(filename, 'rb') as f:
                    query = pickle.load(f)
                    queries.append(query)
            except IsADirectoryError:
                pdb.set_trace()
        pm.go_up()
        return queries

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
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_ADS_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        filenames = os.listdir()
        ads = []
        for filename in filenames:
            if filename == '.DS_Store':
                continue
            try:
                with open(filename, 'rb') as f:
                    ad = pickle.load(f)
                    ads.append(ad)
            except IsADirectoryError:
                pdb.set_trace()
        pm.go_up()
        pm.go_up()
        return ads

