# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_evaluator import TaskGraphEvaluator
from task_graph_node_remover import TaskGraphNodeRemover
from task_graph_edge_finder import TaskGraphEdgeFinder
from task_graph_first_answerer import TaskGraphFirstAnswerer
import pdb

if __name__ == '__main__':
    query = '部屋　掃除する'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    node_remover = TaskGraphNodeRemover(g)
    node_remover.remove_low_score_generalized_tasks()

    query_task = '_'.join(query.split('　'))

    node_selector = TaskGraphFirstAnswerer(graph=g, query_task=task_query)
    node_selector.set_first_result_tasks()
    node_selector.print_subtasks()

    edge_finder = TaskGraphEdgeFinder(node_remover.graph)
    pdb.set_trace()
