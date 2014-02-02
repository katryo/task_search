# -*- coding: utf-8 -*-
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from task_graph_zero_answerer import TaskGraphZeroAnswerer
from answer_printer import AnswererPrinter
from path_mover import PathMover
import constants
import pdb

if __name__ == '__main__':
    queries = ['保育園　入園させる']
    for query in queries:
        pfl = PickleFileLoaderForOriginal()
        pfs = PickleFileSaverForOriginal()
        g = pfl.load_graph_with_query(query)
        query_task = '_'.join(query.split('　'))

        pm = PathMover()

        print('zeroの結果です')

        answerer = TaskGraphZeroAnswerer(graph=g, query_task=query_task)
        answerer.set_result_tasks()
        pfs.save_answerer_with_query(answerer, query)
        answerer.set_task_scores()
        pfs.save_answerer_with_query(answerer, query)
        answerer.set_united_results()
        pfs.save_answerer_with_query(answerer, query)
        printer = AnswererPrinter(answerer=answerer, query=query)

        pm.go_or_create_and_go_to('results')
        pm.go_or_create_and_go_to(query)

        printer.output(method_name='zero')
        pm.go_up()
        pm.go_up()
