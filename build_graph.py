# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver_for_ex import PickleFileSaverForEx
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
import constants


if __name__ == '__main__':
    original_queries = constants.QUERIES_2
    pfs = PickleFileSaverForEx()
    pfl = PickleFileLoaderForExpandedQuery()
    for query in original_queries:
        #if pfs.can_find_graph_with_query(query):
            # continue
        pages = pfl.load_fetched_pages_with_query(query)
        gtm = GraphTaskMapper()

        for i, page in enumerate(pages):
            try:
                for task in page.tasks:
                    gtm.add_node_and_edge_with_task(task)
                print('%i 番目のページ %s のタスクをグラフに追加しました' % (i, page.title))
            except AttributeError:
                break
        print('added all edges!')
        pfs.save_graph_with_query(obj=gtm.graph, query=query)
