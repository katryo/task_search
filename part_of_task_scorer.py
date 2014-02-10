#coding: utf-8
from task_graph_evaluator import TaskGraphEvaluator
from abstract_task_cluster_classifier import AbstractTaskClusterClassifier
import pdb


class PartOfTaskScorer(AbstractTaskClusterClassifier):
    """
    scores[0] => (TaskCluster(
    {'不動産業者_に_確認する', '確認_を_する',
     '掃除_を_する', '明細_を_貰う', '全体_を_拭く'}
     ), 5265.0, 'オフィス')
    """
#-----------part-of------
    def scores(self, pairs_per_subtype):
        task_name_frequency_pairs = []
        for subtype in pairs_per_subtype:
            pairs = pairs_per_subtype[subtype]
            if len(pairs) == 0:
                continue
            result = self._cluster_contribution_url_intersection(pairs, subtype)
            task_name_frequency_pairs.append(result)
        results = self._sorted_by_score(task_name_frequency_pairs)
        return results

    def _cluster_contribution_url_intersection(self, pairs, subtype):
        task_names = {pair[0] for pair in pairs}
        evaluator = TaskGraphEvaluator(self.graph)
        result = (task_names, evaluator.contribution_with_cluster(task_names), subtype)
        return result
