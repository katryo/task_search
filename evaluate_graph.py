# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_evaluator import TaskGraphEvaluator
from task_graph_node_remover import TaskGraphNodeRemover
from task_graph_first_answerer import TaskGraphFirstAnswerer
from task_cluster import TaskCluster
import pdb

if __name__ == '__main__':
    query = '犬　育てる'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    node_remover = TaskGraphNodeRemover(g)
    node_remover.remove_low_score_generalized_tasks()

    query_task = '_'.join(query.split('　'))

    first_answerer = TaskGraphFirstAnswerer(graph=g, query_task=query_task)
    first_answerer.set_result_tasks()
    first_answerer.set_task_scores()
    first_answerer.print_score_of_subtasks()


    #answerer = TaskGraphRecursiveAnswerer(graph=g, query_task='畦_節約する')
    #answerer.set_result_tasks()
    #answerer.print_subtasks()

