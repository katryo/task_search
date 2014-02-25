# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from task_graph_first_answerer import TaskGraphFirstAnswerer
from answer_printer import AnswererPrinter
from path_mover import PathMover
import constants
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_4
    for query in queries:
        pfl = PickleFileLoaderForExpandedQuery()
        #pfl = PickleFileLoaderForOriginal()
        g = pfl.load_graph_with_query(query)
        print('ロードしました')
        noun, cmp, verb = query.split('　')
        query_task = '_'.join([noun, cmp, verb])

        if not g:
            print('%sのグラフが存在しません！' % query)
            pdb.set_trace()
            continue

        if not g.nodes():
            print('%sのグラフに異常があります' % query)
            continue
        query_task = '_'.join(query.split('　'))


        # answererがいらないノードをremoveしてくれてるはず
        first_answerer = TaskGraphFirstAnswerer(graph=g, query_task=query_task)
        print('answererをinstance化しました')
        first_answerer.set_result_tasks()
        print('set_result_tasksをしました')
        first_answerer.set_task_scores()

        # generalized_taskはもう計算の邪魔なので消す
        first_answerer.remove_generalized_tasks()
        first_answerer.set_united_results()
        simple_results = []
        for united_result in first_answerer.united_results:
            tasks = united_result[0][0]
            result_tasks = []
            for task in tasks:
                aspects = first_answerer.graph.node[task]['aspects']
                task_noun = task.split('_')[0]
                task_verb = task.split('_')[2]
                if len(aspects) > 6:
                    if not noun in task_noun:
                        if not verb in task_noun:
                            if not verb in task_verb:
                                if not noun in task_verb:
                                    if not task_noun in verb:
                                        result_tasks.append(task)
            if not result_tasks in simple_results:
                if result_tasks:
                    simple_results.append(result_tasks)
        first_answerer.simple_results = simple_results
        printer = AnswererPrinter(answerer=first_answerer, query=query)

        pm = PathMover()
        pm.go_or_create_and_go_to('results')
        pm.go_or_create_and_go_to(query)

        printer.output(method_name='first')
        pm.go_up()
        pm.go_up()
