# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_saver_for_ex import PickleFileSaverForEx
from task_graph_first_answerer import TaskGraphFirstAnswerer
from answer_printer import AnswererPrinter
from path_mover import PathMover
import constants
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_1
    for query in queries:
        pfl = PickleFileLoaderForExpandedQuery()
        pfs = PickleFileSaverForEx()
        g = pfl.load_graph_with_query(query)
        query_task = '_'.join(query.split('　'))

        pm = PathMover()

        print('firstの結果です')

        first_answerer = TaskGraphFirstAnswerer(graph=g, query_task=query_task)
        first_answerer.set_result_tasks()
        pfs.save_answerer_with_query(first_answerer, query)
        first_answerer.set_task_scores()
        pfs.save_answerer_with_query(first_answerer, query)
        if not first_answerer.graph.nodes:
            pdb.set_trace()
        first_answerer.set_united_results()
        pfs.save_answerer_with_query(first_answerer, query)
        printer = AnswererPrinter(answerer=first_answerer, query=query)

        pm.go_or_create_and_go_to('results')
        pm.go_or_create_and_go_to(query)

        printer.output(method_name='first')
        pm.go_up()
        pm.go_up()
