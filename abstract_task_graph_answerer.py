#coding: utf-8
import pdb
from abstract_task_graph_manager import AbstractTaskGraphManager
from task_graph_node_remover import TaskGraphNodeRemover
from task_search_result_sorter import TaskSearchResultSorter

class AbstractTaskGraphAnswerer(AbstractTaskGraphManager):
    """
    検索結果表示に使う。
    1. すべての「良い」エッジを出す
    2. part-ofの同一階層にあるノードをまとめる
    3. subtype-ofにあるタスクは上位タスクにつなげる
    4. subtype-ofの親ノードと、他の良いノードとは関係のないノード、part-ofの汎化ノードのすべてをinstance-ofとして表示する。
    """

    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph)
        self.query_task = query_task
        node_remover = TaskGraphNodeRemover(graph)
        node_remover.remove_low_score_generalized_tasks()


    def print_subtasks(self):
        print ('*********')
        print ('subtype_of')
        print(self.subtype_of_tasks)
        print ('part_of')
        print(self.part_of_task_clusters)
        print ('instance_of')
        print(self.instance_of_task_clusters)
        print ('*********')

    def print_score_of_subtasks(self):
        print ('*********')
        print ('subtype_of')
        print(self.subtype_of_tasks)
        print ('part_of')
        print(self.part_of_task_clusters_scores)
        print ('instance_of')
        print(self.instance_of_task_clusters_scores)
        print ('*********')

    def set_result_tasks(self):
        self.subtype_of_tasks = self._tasks_in_subtype_of_relation()
        self.part_of_task_clusters = self._task_clusters_in_part_of_relation()
        self.instance_of_task_clusters = self._task_clusters_in_instance_of_relation()

    def set_task_scores(self):
        #override me!!
        pass

    def set_united_results(self):
        sorter = TaskSearchResultSorter(self)
        self.united_results = sorter.sorted_by_mmr()

#-----private------

    def _tasks_in_subtype_of_relation(self):
        # override me !!!
        # zeroではset()を返す
        pass

    def _task_clusters_in_part_of_relation(self):
        # override me !!!
        # zeroでは同じurlのページのタスク集合を返す
        pass

    def _task_clusters_in_instance_of_relation(self):
        # override me !!!
        # zeroではpart-ofでないタスクを{'A_B'}のように、度順に返す
        pass

