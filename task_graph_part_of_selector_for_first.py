#coding: utf-8
from abstract_task_graph_part_of_selector import AbstractTaskGraphPartOfSelector
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
