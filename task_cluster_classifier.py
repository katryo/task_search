#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from task_graph_evaluator import TaskGraphEvaluator
import pdb


class TaskClusterClassifier(AbstractTaskGraphManager):


#-----------part-of------

    def clusters_contribution_url_intersections(self, clusters):
        task_name_frequency_pairs = []
        for cluster in clusters:
            result = self._cluster_contribution_url_intersection(cluster)
            task_name_frequency_pairs.append(result)
        task_name_frequency_pairs.sort(key=lambda result: result[1], reverse=True)
        return task_name_frequency_pairs


#-----------instance-of----

    def instance_of_task_clusters_higher(self, clusters):
        results = self._clusters_contribution_url(clusters)
        return results


#--------ここでcontributionを切り替え

    def _cluster_contribution_url_intersection(self, cluster):
        task_names = {l for l in cluster}
        url_set = set()
        for task_name in task_names:
            #if len(task_name) == 1:
            #    pdb.set_trace()
            aspects = self._aspects_with_task_name(task_name)
            urls = {aspect['url'] for aspect in aspects}
            if not url_set:
                url_set = urls
            else:
                url_set = url_set.intersection(urls)

        evaluator = TaskGraphEvaluator(self.graph)
        # cluster => TaskCluster({'', '', ...})
        result = (cluster, evaluator.contribution(cluster), url_set)
        return result

#-----------part-of------

    def _clusters_contribution_url(self, clusters):
        results = []
        for cluster in clusters:
            result = self._cluster_contribution_url(cluster)
            results.append(result)
        results.sort(key=lambda result: result[1], reverse=True)
        return results

    def _cluster_contribution_url(self, cluster):
        evaluator = TaskGraphEvaluator(self.graph)
        task_names = {l for l in cluster}
        aspects = (self._aspects_with_task_name(task_name) for task_name in task_names)
        try:
            urls = {aspect[0]['url'] for aspect in aspects}
        except IndexError:
            urls = set()
        result = (cluster, evaluator.contribution(cluster), urls)
        return result

#---------zero----------

