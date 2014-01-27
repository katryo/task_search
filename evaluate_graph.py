# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_evaluator import TaskGraphEvaluator
from task_graph_node_remover import TaskGraphNodeRemover
from task_graph_first_answerer import TaskGraphFirstAnswerer
from task_cluster import TaskCluster
import pdb

if __name__ == '__main__':
    query = '家庭菜園　始める'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    query_task = '_'.join(query.split('　'))

    first_answerer = TaskGraphFirstAnswerer(graph=g, query_task=query_task)
    first_answerer.set_result_tasks()
    first_answerer.set_task_scores()
    first_answerer.print_score_of_subtasks()

