# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from task_data_selector import TaskDataSelector
import constants


if __name__ == '__main__':
    original_queries = constants.QUERIES_4
    pfs = PickleFileSaverForOriginal()
    with TaskDataSelector() as selector:
        for query in original_queries:
            # それぞれのクエリで、rankが1-100までのページに属するタスクを集める。
            gtm = GraphTaskMapper()
            tasks = selector.task_set_of_higher_rank_with_query(query)
            for task in tasks:
                gtm.add_node_and_edge_with_task(task)
            pfs.save_graph_with_query(obj=gtm.graph, query=query)
