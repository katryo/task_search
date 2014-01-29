from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pickle
import pdb


class PickleFileLoaderForOriginal(PickleFileLoader):
    def load_fetched_pages_with_original_query(self, query):
        path = os.path.join(constants.FETCHED_PAGES_O_DIR_NAME, query)
        os.chdir(path)
        pm = PathMover()
        pm.go_or_create_and_go_to(query)
        pages = []
        for i in range(constants.NUM_OF_FETCHED_PAGES):
            try:
                with open('%s_%i.pkl' % (query, i), 'rb') as f:
                    page = pickle.load(f)
                    pages.append(page)
            except EOFError:
                break
        os.chdir('../..')
        pm.go_up()
        return pages

    def load_graph_with_query(self, query):
        pm = PathMover()
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        graph = self.load_file(query + '_graph.pkl')
        pm.go_up()
        pm.go_up()
        return graph
