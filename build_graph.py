# -*- coding: utf-8 -*-
import pdb
from posinega_graph_mapper import PosinegaGraphMapper
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
import networkx as nx
import matplotlib.pyplot as plt
import constants


if __name__ == '__main__':
    original_queries = constants.QUERIES_4
    pfs = PickleFileSaverForOriginal()
    pfl = PickleFileLoaderForOriginal()
    for query in original_queries:
        pages = pfl.load_fetched_pages_with_query(query)
        posinega_graph_mapper = PosinegaGraphMapper()

        for i, page in enumerate(pages):
            if -1 < page.rank < 5:
                if page.tasks:
                    posinega_graph_mapper.add_edges_with_page(page)
                    print('%i 番目のページのタスクをグラフに追加しました' % i)
        nx.draw(posinega_graph_mapper.graph)
        plt.show()
        print('added all edges!')
