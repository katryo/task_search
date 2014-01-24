#coding: utf-8
import pdb
from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from task_graph_edge_finder import TaskGraphEdgeFinder
from task_graph_recursive_answerer_hand import TaskGraphRecursiveAnswererHand


class TaskGraphRecursiveAnswerer(AbstractTaskGraphAnswerer):
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        # query_taskがoriginalのときと、generalized_taskのときがある。
        # generalizedのときは、その特化タスクsでやってしまう。

        super().__init__(graph, query_task)
        edge_finder = TaskGraphEdgeFinder(self.graph)

        is_original = edge_finder.guess_original_with_task_name(query_task)
        if is_original:
            self.hands = set(TaskGraphRecursiveAnswererHand(query_task))
            return

        edges = self.graph.edges(query_task)
        specialized_task_names = [edge[1] for edge in edges]
        pdb.set_trace()  # edge[1]かedge[0]かどっちだったか
        self.hands = set()
        for specialized_task_name in specialized_task_names:
            hand = TaskGraphRecursiveAnswererHand(specialized_task_name)
            self.hands.add(hand)

    def _tasks_in_subtype_of_relation(self):
        tasks = set()
        for hand in self.hands:
            tasks_in_hand = hand.tasks_in_subtype_of_relation()
            for task in tasks_in_hand:
                tasks.add(task)
        return tasks


    def _task_clusters_in_part_of_relation(self):
        clusters = []
        for hand in self.hands:
            clusters_in_hand = hand.tasks_in_subtype_of_relation()
            clusters.extend(clusters_in_hand)
        return clusters

    def _tasks_in_instance_of_relation(self):
        task_names = set()
        for hand in self.hands:
            names_in_hand = hand.tasks_in_subtype_of_relation()
            for name in names_in_hand:
                task_names.add(name)
        return task_names

