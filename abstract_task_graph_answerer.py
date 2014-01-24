#coding: utf-8
import pdb
from abstract_task_graph_manager import AbstractTaskGraphManager
from task_graph_edge_finder import TaskGraphEdgeFinder

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
        self.subtype_of_tasks = set()
        self.part_of_task_clusters = []

    def print_subtasks(self):
        print ('*********')
        print ('subtype_of')
        print(self.subtype_of_tasks)
        print ('part_of')
        print(self.part_of_task_clusters)
        print ('instance_of')
        print(self.instance_of_tasks)
        print ('*********')

    def set_result_tasks(self):
        self.subtype_of_tasks = self._tasks_in_subtype_of_relation()
        self.part_of_task_clusters = self._task_clusters_in_part_of_relation()
        self.instance_of_tasks = self._tasks_in_instance_of_relation()

    def _tasks_in_subtype_of_relation(self):
        # 最初のクエリ'部屋_掃除する'に対する'子供部屋_掃除する'のようなものを出力
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_names = edge_finder.subtype_of_edges_lead_to_original_task_with_task_name(self.query_task)
        return task_names

    def _children_of_part_of_task_clusters(self):
        children = set()
        for task_cluster in self.part_of_task_clusters:
            for cluster_name in task_cluster:
                children_names = self.graph.neighbors(cluster_name)
                for child_name in children_names:
                    children.add(child_name)
        return children
