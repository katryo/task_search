# coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from sim_calculator import SimCalculator
from task_graph_evaluator import TaskGraphEvaluator
import constants
import pdb


class SameURLPartOfTaskUniter(AbstractTaskGraphManager):
    def __init__(self, graph=None, task_distance_pairs={'旅館': {('温泉_に_入る', 12), ('湯船_に_つかる', -4)}}):
        super().__init__(graph)
        self.task_distance_pairs = task_distance_pairs

    def unite_recursively(self):
        threshold = constants.THRESHOLD_FOR_REMOVING_FROM_PART_OF  # 0.2くらい
        try:
            cluster_a, cluster_b = self._find_clusters_to_be_united()
        except ValueError:  # []つまり統合すべきタスクなし
            return

        united_new_cluster = cluster_a.union(cluster_b)
        not_shared_tasks = cluster_a.difference(cluster_b).union(cluster_b.difference(cluster_a))

        evaluator = TaskGraphEvaluator(self.graph)
        for task_name in not_shared_tasks:
            contribution = float(evaluator.contribution_with_task_name(task_name)[0])
            average_of_contribution = evaluator.contribution_with_cluster(united_new_cluster) / len(united_new_cluster)
            if contribution < average_of_contribution * threshold:
                print('%sは別ルートの可能性が高いので排除しました' % task_name)
                united_new_cluster.remove(task_name)

        self.task_distance_pairs[constants.SUPERTYPE_NAME].append(united_new_cluster)
        self.task_distance_pairs[constants.SUPERTYPE_NAME].remove(cluster_a)
        self.task_distance_pairs[constants.SUPERTYPE_NAME].remove(cluster_b)
        self.unite_recursively()

    def _find_clusters_to_be_united(self):
        threshold = constants.THRESHOLD_FOR_UNITING_IN_PART_OF  # 0.4くらい
        # すべての組み合わせ（ただしcluster_a自身を除く）で、和をとるべきものを見つけたらその組み合わせを返す
        for cluster_a in self.task_distance_pairs[constants.SUPERTYPE_NAME]:
            for cluster_b in self.task_distance_pairs[constants.SUPERTYPE_NAME]:
                if cluster_a == cluster_b:
                    continue
                nume = len(cluster_a.intersection(cluster_b))
                deno = len(cluster_a.union(cluster_b))
                sim = nume / deno
                if sim > threshold:
                    return [cluster_a, cluster_b]
        return []

