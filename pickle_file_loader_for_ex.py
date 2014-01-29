from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pickle
import pdb


class PickleFileLoaderForEx(PickleFileLoader):
    def load_fetched_pages_of_ex_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        expanded_queries = os.listdir()
        pages = []
        for expanded_query in expanded_queries:
            if expanded_query == '.DS_Store' or 'graph' in expanded_query:
                continue
            pm.go_or_create_and_go_to(expanded_query)
            filenames = os.listdir()
            for i, filename in enumerate(filenames):
                if filename == '.DS_Store' or 'graph' in filename:
                    continue
                page = self.load_file(filename)
                pages.append(page)
            pm.go_up()
        pm.go_up()
        pm.go_up()
        return pages

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

    def load_graph_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        graph = self.load_file(query + '_graph.pkl')
        pm.go_up()
        pm.go_up()
        return graph

    def load_fetched_pages_with_query_and_expansion_word(self, query, expansion_word):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        if expansion_word == '':
            pm.go_or_create_and_go_to(query)
        else:
            pm.go_or_create_and_go_to(query + '　' + expansion_word)

        filenames = os.listdir()
        pages = []
        for filename in filenames:
            if filename == '.DS_Store':
                continue
            try:
                with open(filename, 'rb') as f:
                    page = pickle.load(f)
                    pages.append(page)
            except IsADirectoryError:
                pdb.set_trace()
        pm.go_up()
        pm.go_up()
        pm.go_up()
        return pages

