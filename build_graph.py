# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver import PickleFileSaver
from pickle_file_loader import PickleFileLoader


if __name__ == '__main__':
    query = '部屋　掃除する'
    pfl = PickleFileLoader()
    pages = pfl.load_fetched_pages_of_ex_with_query(query)
    gtm = GraphTaskMapper()

    for page in pages:
        for task in page.tasks:
            gtm.add_node_and_edge_with_task(task)
        print('Tasks on %s are added!' % page.title)
    print('added all edges!')
    pfs = PickleFileSaver()
    pfs.save_graph_with_query(obj=gtm.graph, query=query)
