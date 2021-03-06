#coding: utf-8
from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pdb


class PickleFileLoaderForExpandedQuery(PickleFileLoader):
    def load_fetched_pages_with_query(self, query):
        pages = self._load_with_query_and_dirname(query, constants.FETCHED_PAGES_DIR_NAME)
        return pages

    def load_pages_with_task_with_query(self, query):
        pages = self._load_with_query_and_dirname(query, constants.FETCHED_PAGES_WITH_TASK_FOR_EX_DIR_NAME)
        return pages

    def _load_with_query_and_dirname(self, query, dirname_for_pages):
        pages = []
        original_query_dirpath = os.path.join(dirname_for_pages, query)
        for d_dirpath, d_dirnames, d_filenames in os.walk(original_query_dirpath):
            for expanded_query in d_dirnames:
                expanded_query_dirpath = os.path.join(d_dirpath, expanded_query)
                for d_d_dirpath, d_d_dirnames, d_d_filenames in os.walk(expanded_query_dirpath):
                    pdb.set_trace()
                    for i, filename in enumerate(d_d_filenames):
                        if filename == '.DS_Store':
                            continue
                        try:
                            filepath = os.path.join(d_d_dirpath, filename)
                            page = self.load_file(filepath)
                            print('%sのロードに成功しました！' % filename)
                            pages.append(page)
                            if len(pages) == constants.NUM_OF_PAGE_PER_QUERY:
                                return pages
                        except EOFError:
                            print('%sのロードに失敗しました！' % filename)
        # return pages

    def load_graph_with_query(self, query):
        filepath = os.path.join(constants.GRAPH_DIR_NAME, query, query + '_graph_first.pkl')
        graph = self.load_file(filepath)
        return graph

    def load_answerer_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.ANSWERER_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        graph = self.load_file(query + '_answerer_first.pkl')
        pm.go_up()
        pm.go_up()
        return graph

