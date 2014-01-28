#coding: utf-8
import pdb
from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from task_graph_edge_finder import TaskGraphEdgeFinder
from task_cluster import TaskCluster
from task_cluster_classifier_for_first import TaskClusterClassifierForFirst
from task_graph_part_of_selector_for_first import TaskGraphPartOfSelectorForFirst
from task_graph_instance_of_selector import TaskGraphInstanceOfSelector
from part_of_task_uniter import PartOfTaskUniter

class TaskGraphFirstAnswerer(AbstractTaskGraphAnswerer):
    """
    部分的に改良した手法と全部改良した手法
    """
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph=graph, query_task=query_task)
        self.frequent_original_tasks = self._frequent_original_tasks()

    def set_task_scores(self):
        classifier = TaskClusterClassifierForFirst(self.graph)
        self.part_of_task_clusters_scores = classifier.clusters_contribution_url_intersections(self.part_of_task_clusters)
        self.instance_of_task_clusters_scores = classifier.instance_of_task_clusters_higher(self.instance_of_task_clusters)

#-------private----------
    def _frequent_original_tasks(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        results = set()
        for generalized_task in task_names_with_higher_score:
            good_original_task_names = self.graph.predecessors(generalized_task)
            good_original_tasks = []
            for task_name in good_original_task_names:
                task_attr_dict = self.graph.node[task_name]
                task_attr_dict['name'] = task_name
                good_original_tasks.append(task_attr_dict)

            # もうここにfreqを淹れればよいのでは
            for good_original_task in good_original_tasks:
                results.add(good_original_task['name'])
        return results

    def _task_names_in_score_higher_than(self, num=1):
        scores = self.graph.in_degree()  # {'調味料_ばらまく': 1, ...}
        results = [name for name in scores if scores[name] > num]
        return results  # original_taskはほとんどない。

#---------------subtype-of------------

    def _tasks_in_subtype_of_relation(self):
        # 最初のクエリ'部屋_掃除する'に対する'子供部屋_掃除する'のようなものを出力
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_names = edge_finder.subtype_of_edges_lead_to_original_task_with_task_name(self.query_task)
        return task_names

#---------------part-of------------

    def _task_clusters_in_part_of_relation(self):
        selector = TaskGraphPartOfSelectorForFirst(self.graph,
                                                   candidate_tasks=self.frequent_original_tasks,
                                                   subtype_of_tasks=self.subtype_of_tasks)
        task_names = selector._frequent_tasks_which_are_not_subtype_of()
        task_clusters = selector.part_of_task_clusters_with_task_names(task_names)
        uniter = PartOfTaskUniter(graph=self.graph, task_clusters=task_clusters)
        task_clusters = uniter.unite()
        return task_clusters
#---------------instance-of------------

    def _task_clusters_in_instance_of_relation(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        task_clusters = []  # [{'a_b', 'a_c', ...}]
        # ひとつでも共通するタスクがあればtask_clusterは貪欲にとりこんでいく
        for generalized_task in task_names_with_higher_score:
            good_original_task_names = self.graph.predecessors(generalized_task)
            if good_original_task_names:
                selector = TaskGraphInstanceOfSelector(graph=self.graph,
                                                       candidate_tasks=self.frequent_original_tasks,
                                                       subtype_of_tasks=self.subtype_of_tasks,
                                                       part_of_tasks_clusters=self.part_of_task_clusters)
                good_original_task_names = selector.task_names_only_instance_of_with_task_names(good_original_task_names)
                if good_original_task_names:
                    task_cluster = TaskCluster(good_original_task_names)
                    i_clusters = task_cluster.i_cluster_shares_task_with_clusters(task_clusters)
                    if i_clusters == -1:
                        task_clusters.append(task_cluster)
                        continue
                        # ここでTaskClusterオブジェクトではなくsetオブジェクトになる。
                    task_clusters[i_clusters] = TaskCluster(task_clusters[i_clusters].union(task_cluster))
        return task_clusters

