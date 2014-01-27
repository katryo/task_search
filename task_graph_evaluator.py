#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class TaskGraphEvaluator(AbstractTaskGraphManager):
    def appearance_count_with_task_cluster(self, task_cluster):
        num_of_appearance = 0
        for task_name in task_cluster:
            aspects = self._aspects_with_task_name(task_name)
            num_of_appearance += len(aspects)
        return num_of_appearance

    def contribution(self,
                     task_cluster,
                     multiplier_for_official=2.0,
                     multiplier_for_shopping=0.5):
        score_for_task_cluster = 0
        used_urls = set()
        for task_name in task_cluster:
            aspects = self._aspects_with_task_name(task_name)
            for aspect in aspects:
                score_for_aspect = 1
                if aspect['is_official']:
                    score_for_aspect *= multiplier_for_official
                if aspect['is_shopping']:
                    score_for_aspect *= multiplier_for_shopping
                score_for_task_cluster += score_for_aspect
                used_urls.add(aspect['url'])
        score_for_task_cluster *= len(used_urls)
        score_for_task_cluster /= len(task_cluster)
        print('%sの貢献度計算完了！' % task_cluster)
        return score_for_task_cluster
