#coding: utf-8
from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pdb


class PickleFileLoaderForExpandedQuery(PickleFileLoader):
    def load_fetched_pages_with_query(self, query):
        pages = []
        for dirpath, dirnames, filenames in os.walk(constants.FETCHED_PAGES_DIR_NAME):
            original_query_dirpath = os.path.join(dirpath, query)
            for d_dirpath, d_dirnames, d_filenames in os.walk(original_query_dirpath):
                for expanded_query in d_dirnames:
                    expanded_query_dirpath = os.path.join(d_dirpath, expanded_query)
                    for d_d_dirpath, d_d_dirnames, d_d_filenames in os.walk(expanded_query_dirpath):
                        for i, filename in enumerate(d_d_filenames):
                            if filename == '.DS_Store':
                                continue
                            try:
                                filepath = os.path.join(d_d_dirpath, filename)
                                page = self.load_file(filepath)
                                print('%sのロードに成功しました！' % filename)
                                pages.append(page)
                            except EOFError:
                                print('%sのロードに失敗しました！' % filename)
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

