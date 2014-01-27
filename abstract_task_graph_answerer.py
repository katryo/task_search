#coding: utf-8
import pdb
from abstract_task_graph_manager import AbstractTaskGraphManager

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

    def _children_of_part_of_task_clusters(self):
        children = set()
        for task_cluster in self.part_of_task_clusters:
            for task_name in task_cluster:
                children.add(task_name)
        return children

    def set_result_tasks(self):
        self.subtype_of_tasks = self._tasks_in_subtype_of_relation()
        self.part_of_task_clusters = self._task_clusters_in_part_of_relation()
        self.instance_of_task_clusters = self._task_clusters_in_instance_of_relation()

