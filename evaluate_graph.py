# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from task_graph_first_answerer import TaskGraphFirstAnswerer
from task_graph_zero_answerer import TaskGraphZeroAnswerer
from answer_printer import AnswererPrinter
import pdb

if __name__ == '__main__':
    query = 'ビリヤード　優勝する'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    query_task = '_'.join(query.split('　'))

    print('zeroの結果です')

    zero_answerer = TaskGraphZeroAnswerer(graph=g, query_task=query_task)
    zero_answerer.set_result_tasks()
    zero_answerer.set_task_scores()

    printer = AnswererPrinter(answerer=zero_answerer, query=query)
    printer.ourput(method_name='zero')

    print('firstの結果です')

    first_answerer = TaskGraphFirstAnswerer(graph=g, query_task=query_task)
    first_answerer.set_result_tasks()
    first_answerer.set_task_scores()
    first_answerer.print_score_of_subtasks()
