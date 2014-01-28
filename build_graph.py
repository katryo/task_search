# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver import PickleFileSaver
from pickle_file_loader import PickleFileLoader
import constants


if __name__ == '__main__':
    original_queries = ['来客　もてなす']
    for query in original_queries:
        pfl = PickleFileLoader()
        pages = pfl.load_fetched_pages_of_ex_with_query(query)
        gtm = GraphTaskMapper()

        for i, page in enumerate(pages):
            try:
                print(len(page.sentences))
                for task in page.tasks:
                    gtm.add_node_and_edge_with_task(task)
                print('%i 番目のページ %s のタスクをグラフに追加しました' % (i, page.title))
            except AttributeError:
                break
        print('added all edges!')
        pfs = PickleFileSaver()
        pfs.save_graph_with_query(obj=gtm.graph, query=query)
