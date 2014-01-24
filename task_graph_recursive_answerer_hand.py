import pdb
from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from task_graph_edge_finder import TaskGraphEdgeFinder


class TaskGraphRecursiveAnswererHand(AbstractTaskGraphAnswerer):
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph, query_task)
        edge_finder = TaskGraphEdgeFinder(self.graph)
        self.part_of_children_task_names = edge_finder.part_of_edges_with_task_name(self.query_task)

    def tasks_in_subtype_of_relation(self):
        # 最初のクエリ'部屋_掃除する'に対する'子供部屋_掃除する'のようなものを出力
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_names = edge_finder.subtype_of_edges_lead_to_original_task_with_task_name(self.query_task)
        return task_names

    def task_clusters_in_part_of_relation(self):
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_clusters = []
        for task_name in self.part_of_children_task_names:
            task_cluster = edge_finder.part_of_edges_with_task_name(task_name)
            task_clusters.append(task_cluster)
        return task_clusters

    def tasks_in_instance_of_relation(self):
        task_names = self.part_of_children_task_names
        for subtype_of_task in self.subtype_of_tasks:
            task_names.remove(subtype_of_task)

        children_of_part_of_task_clusters = self._children_of_part_of_task_clusters()
        for child in children_of_part_of_task_clusters:
            try:
                task_names.remove(child)
            except KeyError:  # もうchildは削除されているとき
                continue
        return task_names
