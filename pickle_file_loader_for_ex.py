#coding: utf-8
from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pdb


class PickleFileLoaderForExpandedQuery(PickleFileLoader):
    def load_fetched_pages_with_query(self, query):
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
                try:
                    page = self.load_file(filename)
                    print('%sのロードに成功しました！' % filename)
                    pages.append(page)
                except EOFError:
                    print('%sのロードに失敗しました！' % filename)
            pm.go_up()
        pm.go_up()
        pm.go_up()
        return pages

    def load_graph_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.GRAPH_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        graph = self.load_file(query + '_graph_first.pkl')
        pm.go_up()
        pm.go_up()
        return graph

    def load_answerer_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.ANSWERER_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        graph = self.load_file(query + '_answerer_first.pkl')
        pm.go_up()
        pm.go_up()
        return graph

