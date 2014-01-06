# -*- coding: utf-8 -*-
import utils
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver import PickleFileSaver


if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    gtm = GraphTaskMapper()

    for page in pages:
        for task in page.tasks:
            gtm.add_node_and_edge_with_task(task)
    print('added all edges!')
    results_dic = gtm.broader_nodes_with_higher_in_degree_score()
    pfs = PickleFileSaver()
    pfs.save_simple_task_search_result(results_dic)