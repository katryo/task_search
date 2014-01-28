from abstract_task_graph_manager import AbstractTaskGraphManager
from sim_calculator import SimCalculator


class PartOfTaskUniter(AbstractTaskGraphManager):
    def __init__(self, graph=None, task_clusters={}):
        supter().__init__(graph)
        self.task_clusters = task_clusters

    def unite(self):
        self._unite_recursively()
        return self.task_clusters

    def _unite_recursively(self):
        threshold = 0.5
        try:
            cluster_a, cluster_b = self._find_clusters_to_be_united()
        except ValueError:  # []つまり統合すべきタスクなし
            return

        united_new_cluster = cluster_a.union(cluster_b)
        not_shared_tasks = cluster_a.difference(cluster_b).union(cluster_b.diffecrence(cluster_a))

        for task_name in not_shared_tasks:
            if score(task_name) < (sum_of_scores(united_new_cluster) / len(united_new_cluster)) * threshold:
                united_new_cluster.remove(task_name)

        self.task_clusters.add(united_new_cluster)
        self.task_clusters.remove(cluster_a)
        self.task_clusters.remove(cluster_b)
        self._unite_recursively()

    def _find_clusters_to_be_united(self):
        sim_calculator = SimCalculator(self.graph)
        for cluster_a in self.task_clusters:
            for cluster_b in self.task_clusters.difference(set([cluster_a])):
                if sim_calculator.similarity(cluster_a, cluster_b) > 0.5:
                    return [cluster_a, cluster_b]
        return []

