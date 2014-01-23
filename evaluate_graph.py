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
    edge_finder = TaskGraphEdgeFinder(g)
    pdb.set_trace()
