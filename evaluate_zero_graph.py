# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from task_graph_zero_answerer import TaskGraphZeroAnswerer
from answer_printer import AnswererPrinter
from path_mover import PathMover
import constants
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_4
    for query in queries:
        pfl = PickleFileLoaderForOriginal()
        g = pfl.load_graph_with_query(query)
        noun, cmp, verb = query.split('　')
        query_task = '_'.join([noun, cmp, verb])

        pm = PathMover()

        print('zeroの結果です')

        answerer = TaskGraphZeroAnswerer(graph=g, query_task=query_task)
        print('zero_answererをinstance化しました')
        answerer.set_result_tasks()
        print('set_result_tasks')
        answerer.set_task_scores()
        print('set_task_scores')
        answerer.set_united_results()
        simple_results = []
        for united_result in answerer.united_results:
            tasks = united_result[0][0]
            result_tasks = []
            for task in tasks:
                aspects = answerer.graph.node[task]['aspects']
                task_noun = task.split('_')[0]
                task_verb = task.split('_')[2]
                if len(aspects) > 2:
                    if not noun in task_noun:
                        if not verb in task_noun:
                            if not verb in task_verb:
                                if not noun in task_verb:
                                    if not task_noun in verb:
                                        result_tasks.append(task)
            if not result_tasks in simple_results:
                if result_tasks:
                    simple_results.append(result_tasks)
        answerer.simple_results = simple_results
        printer = AnswererPrinter(answerer=answerer, query=query)

        pm.go_or_create_and_go_to('results')
        pm.go_or_create_and_go_to(query)


        printer.output(method_name='zero')
        pm.go_up()
        pm.go_up()
