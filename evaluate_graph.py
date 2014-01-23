# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_evaluator import TaskGraphEvaluator
from graph_task_mapper import GraphTaskMapper
import pdb

if __name__ == '__main__':
    query = '部屋　掃除する'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    #tge = TaskGraphEvaluator(g)
    #tge.evaluate()
    gtm = GraphTaskMapper(g)
    gtm.remove_low_score_generalized_tasks()
    pdb.set_trace()
    for generalized_task in good_original_tasks_by_generalized_tasks:
        print(generalized_task)
        print('original tasks are')
        print(good_original_tasks_by_generalized_tasks[generalized_task])
