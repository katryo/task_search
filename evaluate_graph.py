# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_evaluator import TaskGraphEvaluator
from task_graph_node_remover import TaskGraphNodeRemover
from graph_task_mapper import GraphTaskMapper
from task_graph_edge_finder import TaskGraphEdgeFinder
import pdb

if __name__ == '__main__':
    query = '部屋　掃除する'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    node_remover = TaskGraphNodeRemover(g)
    node_remover.remove_low_score_generalized_tasks()
    task_names = node_remover.graph.nodes()
    edge_finder = TaskGraphEdgeFinder(node_remover.graph)
    for task_name in task_names:
        edges = edge_finder.subtype_of_edges_lead_to_original_task_with_task_name(task_name)
        if edges:
            print('***')
            print(task_name)
            print('is subtype-of')
            print(edges)
            print('are in the same page')
            print('***')

