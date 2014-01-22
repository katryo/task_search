# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_evaluator import TaskGraphEvaluator


if __name__ == '__main__':
    query = '掃除　方法'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    tge = TaskGraphEvaluator(g)
    tge.evaluate()
