import math
from task_graph_similar_node_finder import TaskGraphSimilarNodeFinder


class SimCalculator(object):
    def __init__(self, graph):
        self.graph = graph

    # a_set => {'夢_見つける', '未来_待つ'
    def similarity(self, a_set, b_set):
        num_of_similar_task = self._num_of_similar_task(a_set, b_set)
        num_of_union = len(a_set.union(b_set))
        return num_of_similar_task / num_of_union

    def _num_of_similar_task(self, a_set, b_set):
        num_of_similar_task = 0
        node_finder = TaskGraphSimilarNodeFinder(self.graph)
        for b_task in b_set:
            for a_task in a_set:
                tasks_similar_to_a = node_finder.similar_nodes_with_task_name(a_task)
                tasks_similar_to_a.add(a_task)  # 自分自身
                if b_task in tasks_similar_to_a:
                    num_of_similar_task += 1
        return num_of_similar_task


