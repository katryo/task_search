#coding: utf-8
from abstract_task_graph_part_of_selector import AbstractTaskGraphPartOfSelector
from task_graph_edge_finder import TaskGraphEdgeFinder
from task_cluster import TaskCluster
import constants
import pdb


class TaskGraphPartOfSelectorForFirst(AbstractTaskGraphPartOfSelector):
    def task_distance_pairs(self):
        """
        self.subtype_of_tasksごとにsetにしたtask_clustersを返す
        """
        task_clusters = {}
        # {'サロン': {'渋谷の部屋_を_探す', ...}, 'オフィス': {}, ...}
        for subtype_noun in self.subtype_of_tasks:
            # 高頻度の、subtypeでない、オリジナルのタスクの集合から、同じurlのものかentailment関係にあるものを見つける
            for task_name in self.candidate_tasks:
                aspects = self._aspects_with_task_name(task_name)
                for aspect in aspects:
                    dists = aspect['distance_between_subtypes']
                    for dist in dists:
                        if dist == subtype_noun:
                            distance = dists[dist]
                            if subtype_noun in task_clusters:
                                task_clusters[subtype_noun].add((task_name, distance))
                            else:
                                task_clusters[subtype_noun] = set([(task_name, distance)])
        return task_clusters

#----同じURLでのPART-OF

    def part_of_task_clusters_with_task_names(self, task_names):
        SUPERTYPE_NAME = constants.SUPERTYPE_NAME
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_clusters = {SUPERTYPE_NAME: []}  # {'SUPERTYPE': [{'a_b', 'c_d'}, {e_f, 'g_h'}]}
        # 高頻度の、subtypeでない、オリジナルのタスクの集合から、同じurlのものかentailment関係にあるものを見つける
        for task_name in task_names:
            task_names_list = edge_finder.part_of_edges_with_task_name(task_name)
            for task_names in task_names_list:
                task_cluster = TaskCluster(list(task_names))
                if task_cluster in task_clusters[SUPERTYPE_NAME]:  # 重複して数えているのを排除
                    continue
                if task_cluster:
                    if len(task_cluster) > 1:  # 1ページに1つだけタスク記述あるときはpart-ofでない
                        task_clusters[SUPERTYPE_NAME].append(task_cluster)
        return task_clusters

    def _frequent_tasks_which_are_not_subtype_of(self):
        frequent_tasks = self.candidate_tasks
        for subtype_of_task in self.subtype_of_tasks:
            try:
                frequent_tasks.remove(subtype_of_task)
            except KeyError:  # subtype_of_taskがfrequentじゃないとき
                continue
        return frequent_tasks
