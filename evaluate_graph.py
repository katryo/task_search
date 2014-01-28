# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_first_answerer import TaskGraphFirstAnswerer
from task_graph_zero_answerer import TaskGraphZeroAnswerer
import pdb

if __name__ == '__main__':
    query = 'ビリヤード　優勝する'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    query_task = '_'.join(query.split('　'))

    zero_answerer = TaskGraphZeroAnswerer(graph=g, query_task=query_task)
    zero_answerer.set_result_tasks()
    zero_answerer.set_task_scores()
    zero_answerer.print_score_of_subtasks()

    #first_answerer = TaskGraphFirstAnswerer(graph=g, query_task=query_task)
    #first_answerer.set_result_tasks()
    #first_answerer.set_task_scores()
    #first_answerer.print_score_of_subtasks()
