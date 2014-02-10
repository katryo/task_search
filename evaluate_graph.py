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
        print('ロードしました')

        if not g:
            print('%sのグラフが存在しません！' % query)
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
        pfs.save_answerer_with_query(first_answerer, query)
        first_answerer.set_task_scores()
        pfs.save_answerer_with_query(first_answerer, query)

        # generalized_taskはもう計算の邪魔なので消す
        first_answerer.remove_generalized_tasks()
        first_answerer.set_united_results()
        printer = AnswererPrinter(answerer=first_answerer, query=query)

        pm = PathMover()
        pm.go_or_create_and_go_to('results')
        pm.go_or_create_and_go_to(query)

        printer.output(method_name='first')
        pm.go_up()
        pm.go_up()
