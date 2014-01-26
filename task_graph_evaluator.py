#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class TaskGraphEvaluator(AbstractTaskGraphManager):
    def contribution(self, task_cluster):
        """
        task_clusterの貢献度に近いものを求める
        """
        multiplier_for_official_page = 2
        multiplier_for_shopping_page = 0.5
        score_for_task_cluster = 0
        used_urls = set()
        for task_name in task_cluster:
            aspects = self._aspects_with_task_name(task_name)
            for aspect in aspects:
                score_for_aspect = 1
                if aspect['is_official']:
                    score_for_aspect *= multiplier_for_official_page
                if aspect['is_shopping']:
                    score_for_aspect *= multiplier_for_shopping_page
                score_for_task_cluster += score_for_aspect
                used_urls.add(aspect['url'])
        score_for_task_cluster *= len(used_urls)
        return score_for_task_cluster

    def appearance_count_with_task_cluster(self, task_cluster):
        num_of_appearance = 0
        for task_name in task_cluster:
            aspects = self._aspects_with_task_name(task_name)
            num_of_appearance += len(aspects)
        return num_of_appearance

