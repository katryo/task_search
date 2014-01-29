# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from task_graph_first_answerer import TaskGraphFirstAnswerer
from task_graph_zero_answerer import TaskGraphZeroAnswerer
from answer_printer import AnswererPrinter
from path_mover import PathMover
import pdb

if __name__ == '__main__':
    query = '小学校　受験させる'
    pfl = PickleFileLoaderForExpandedQuery()
    g = pfl.load_graph_with_query(query)
    query_task = '_'.join(query.split('　'))

    pm = PathMover()

    pm.go_or_create_and_go_to('results')
    pm.go_or_create_and_go_to(query)

    print('firstの結果です')

    first_answerer = TaskGraphFirstAnswerer(graph=g, query_task=query_task)
    first_answerer.set_result_tasks()
    first_answerer.set_task_scores()
    first_answerer.set_united_results()
    printer = AnswererPrinter(answerer=first_answerer, query=query)
    printer.output(method_name='first')
    pm.go_up()
    pm.go_up()
