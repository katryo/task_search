# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_saver_for_ex import PickleFileSaverForEx
from answer_printer import AnswererPrinter
from path_mover import PathMover
import constants
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_1
    for query in queries:
        pfl = PickleFileLoaderForExpandedQuery()
        pfs = PickleFileSaverForEx()

        pm = PathMover()

        answerer = pfl.load_answerer_with_query(query)
        if not hasattr(answerer, 'subtype_of_tasks'):
            answerer.set_result_tasks()
            pfs.save_answerer_with_query(answerer, query)

        if not hasattr(answerer, 'instance_of_task_clusters_scores'):
            answerer.set_task_scores()
            pfs.save_answerer_with_query(answerer, query)

        if not hasattr(answerer, 'united_results'):
            answerer.set_united_results()
            pfs.save_answerer_with_query(answerer, query)

        pm.go_or_create_and_go_to('results')
        pm.go_or_create_and_go_to(query)

        printer = AnswererPrinter(answerer=answerer, query=query)
        printer.output(method_name='first')
        pm.go_up()
        pm.go_up()
