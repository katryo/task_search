#coding: utf-8
from task_cluster import TaskCluster
from task_graph_edge_finder import TaskGraphEdgeFinder
from abstract_task_graph_part_of_selector import AbstractTaskGraphPartOfSelector


class TaskGraphPartOfSelector(AbstractTaskGraphPartOfSelector):
    def _part_of_task_clusters_with_task_names(self, task_names):
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_clusters = []  # [{'a_b', 'c_d'}, {e_f, 'g_h'}]
        # 高頻度の、subtypeでない、オリジナルのタスクの集合から、同じurlのものかentailment関係にあるものを見つける
        for task_name in task_names:
            task_names_list = edge_finder.part_of_edges_lead_to_original_node_with_task_name(task_name)
            for task_names in task_names_list:
                task_cluster = TaskCluster(list(task_names))
                if task_cluster in task_clusters:  # 重複して数えているのを排除
                    continue
                if task_cluster:
                    if len(task_cluster) > 1:  # 1ページに1つだけタスク記述あるときはpart-ofでない
                        task_clusters.append(task_cluster)
        return task_clusters
