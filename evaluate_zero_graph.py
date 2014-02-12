# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_saver_for_ex import PickleFileSaverForEx
from task_graph_zero_answerer import TaskGraphZeroAnswerer
from answer_printer import AnswererPrinter
from path_mover import PathMover
import constants
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_4
    for query in queries:
        pfl = PickleFileLoaderForExpandedQuery()
        pfs = PickleFileSaverForEx()
        g = pfl.load_graph_with_query(query)
        query_task = '_'.join(query.split('　'))

        pm = PathMover()

        print('zeroの結果です')

        answerer = TaskGraphZeroAnswerer(graph=g, query_task=query_task)
        print('zero_answererをinstance化しました')
        answerer.set_result_tasks()
        print('set_result_tasks')
        pfs.save_answerer_with_query(answerer, query)
        answerer.set_task_scores()
        print('set_task_scores')
        pfs.save_answerer_with_query(answerer, query)
        answerer.set_united_results()
        print('set_united_results')
        pfs.save_answerer_with_query(answerer, query)
        printer = AnswererPrinter(answerer=answerer, query=query)

        pm.go_or_create_and_go_to('results')
        pm.go_or_create_and_go_to(query)


        printer.output(method_name='zero')
        pm.go_up()
        pm.go_up()
