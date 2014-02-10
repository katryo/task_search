# coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from sim_calculator import SimCalculator
from task_graph_evaluator import TaskGraphEvaluator
import constants
import copy
import pdb


class PartOfTaskUniter(AbstractTaskGraphManager):
    """
    subtypeごとにまとめて、頻度と距離でフィルタリングする。
    1. そもそもタスク数の少ないsubtypeは除外すべき。
    なぜならノイズのsubtypeである可能性が高いから。
    しかし、どうせ最後のscore計算ではじかれる。
    2. frequencyの少ないタスクは除外すべき。ノイズの可能性が高い。
    3. 遠いタスクも除外すべき。
    4. ありふれすぎたタスクも、もういちど除外しては？
    """
    def __init__(self, graph=None, task_distance_pairs={'旅館': {('温泉_に_入る', 12), ('湯船_に_つかる', -4)}}):
        super().__init__(graph)
        self.task_distance_pairs = task_distance_pairs

    def unite(self):
        for subtype in self.task_distance_pairs:
            self._remove_far_tasks_with_subtype(subtype)
        pdb.set_trace()
        return self.task_distance_pairs

    def _remove_far_tasks_with_subtype(self, subtype):
        pairs = copy.deepcopy(self.task_distance_pairs)
        for pair in pairs[subtype]:
            distance = pair[1]
            if distance > constants.THRESHOLD_DISTANCE_FOR_REMOVING_FROM_PART_OF:
                self.task_distance_pairs[subtype].remove(pair)
            if distance * 2 < - constants.THRESHOLD_DISTANCE_FOR_REMOVING_FROM_PART_OF:
                self.task_distance_pairs[subtype].remove(pair)



#---------旧式---------

    def _unite_recursively(self):
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

        self.task_clusters.append(united_new_cluster)
        self.task_clusters.remove(cluster_a)
        self.task_clusters.remove(cluster_b)
        self._unite_recursively()

    def _find_clusters_to_be_united(self):
        threshold = constants.THRESHOLD_FOR_UNITING_IN_PART_OF  # 0.4くらい
        # すべての組み合わせ（ただしcluster_a自身を除く）で、和をとるべきものを見つけたらその組み合わせを返す
        sim_calculator = SimCalculator(self.graph)
        for cluster_a in self.task_clusters:
            for cluster_b in self.task_clusters:
                if cluster_a == cluster_b:
                    continue
                if sim_calculator.similarity(cluster_a, cluster_b) > threshold:
                    return [cluster_a, cluster_b]
        return []

