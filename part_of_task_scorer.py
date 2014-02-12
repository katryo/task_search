#coding: utf-8
from task_graph_evaluator import TaskGraphEvaluator
from abstract_task_cluster_classifier import AbstractTaskClusterClassifier
import pdb
import constants

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
            if subtype == constants.SUPERTYPE_NAME:
                for cluster in pairs_per_subtype[subtype]:
                    result = self._cluster_contribution_url_intersection(cluster)
                    task_name_frequency_pairs.append(result)

            else:
                pairs = pairs_per_subtype[subtype]
                if len(pairs) == 0:
                    continue
                result = self._select_subtype_tasks(pairs, subtype)
                task_name_frequency_pairs.append(result)
        results = self._sorted_by_score(task_name_frequency_pairs)
        return results

    def _cluster_contribution_url_intersection(self, cluster):
        task_names = {l for l in cluster}
        url_set = set()
        for task_name in task_names:
            aspects = self._aspects_with_task_name(task_name)
            urls = {aspect['url'] for aspect in aspects}
            if not url_set:
                url_set = urls
            else:
                url_set = url_set.intersection(urls)

        evaluator = TaskGraphEvaluator(self.graph)
        # cluster => TaskCluster({'', '', ...})
        result = (cluster, evaluator.contribution_with_cluster(cluster), url_set)
        return result

    def _select_subtype_tasks(self, pairs, subtype):
        """
        SUBTYPEがあるときのみ使う
        pairs => {('ハウスクリーニング_を_利用する', 25),
        ('新聞_も_分別する', -33), ('ブランド_を_教える', -18)}
        """
        try:
            task_names = {pair[0] for pair in pairs}
        except TypeError:
            pdb.set_trace()
        evaluator = TaskGraphEvaluator(self.graph)
        result = (task_names, evaluator.contribution_with_cluster(task_names), subtype)
        return result

