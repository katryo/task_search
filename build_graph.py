# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
import constants


if __name__ == '__main__':
    original_queries = constants.QUERIES_4
    pfs = PickleFileSaverForOriginal()
    pfl = PickleFileLoaderForOriginal()
    for query in original_queries:
        counter = 0
        pages = pfl.load_fetched_pages_with_query(query)
        gtm = GraphTaskMapper()

        for i, page in enumerate(pages):
            for task in page.tasks:
                counter += 1
                gtm.add_node_and_edge_with_task(task)
            print('%i 番目のページのタスクをグラフに追加しました' % i)
        print('added all edges!')
        print('%iです' % counter)
        pfs.save_graph_with_query(obj=gtm.graph, query=query)
