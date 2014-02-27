#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from networkx.exception import NetworkXError
from posinega_evaluator import PosinegaEvaluator
import pdb


class TaskGraphEvaluator(AbstractTaskGraphManager):
    def appearance_count_with_task_cluster(self, task_cluster):
        num_of_appearance = 0
        for task_name in task_cluster:
            aspects = self._aspects_with_task_name(task_name)
            num_of_appearance += len(aspects)
        return num_of_appearance

    def score_with_task_name(self, task_name):
        return self.contribution_with_task_name(task_name)

    def frequency_with_task_name(self, task_name):
        score_for_task = 0.0
        same_task_names = set()
        generalized_task_names = self.graph.out_edges(task_name)
        for generalized_task in generalized_task_names:
            try:
                for same_task in self.graph.predecessors(generalized_task[0]):
                    print('同じタスクを発見！')
                    same_task_names.add(same_task)
            except NetworkXError:
                continue
        used_urls = set()
        if not same_task_names:
            same_task_names.add(task_name)
        for same_task in same_task_names:
            aspects = self._aspects_with_task_name(same_task)
            for aspect in aspects:
                score_for_task += 1
                used_urls.add(aspect['url'])
        print('%sの貢献度は%fです' % (task_name, score_for_task))
        return score_for_task, used_urls

    # 1タスクノードの貢献度
    def contribution_with_task_name(self,
                                    task_name):
        aspects = self._aspects_with_task_name(task_name)
        score_for_task = 0.0
        used_urls = set()
        for aspect in aspects:
            evaluator = PosinegaEvaluator()
            score_for_aspect = evaluator.score_of_sentence(aspect['sentence'])
            #score_for_aspect = 1  # ここをposinegaでやってみる？
            score_for_task += score_for_aspect
            used_urls.add(aspect['url'])
        print('%sの貢献度は%fです' % (task_name, score_for_task))
        return score_for_task, used_urls

    # 1クラスターの貢献度
    def contribution_with_cluster(self,
                                  task_cluster):
        score_for_task_cluster = 0
        used_urls = set()
        for task_name in task_cluster:
            [score_for_task,
             used_urls_per_task] = self.contribution_with_task_name(task_name)
            score_for_task_cluster += score_for_task
            used_urls = used_urls.union(used_urls_per_task)
        score_for_task_cluster *= len(used_urls)
        # 大きなpart-ofを高く評価するためコメントアウトしてみる
        # score_for_task_cluster /= len(task_cluster)
        print('%sの頻度計算完了！' % task_cluster)
        return score_for_task_cluster

    def contribution_without_official(self, task_cluster):
        scores = self.contribution_with_cluster(task_cluster,
                                                multiplier_for_official=1)
        return scores

    def contribution_without_shopping(self, task_cluster):
        scores = self.contribution_with_cluster(task_cluster,
                                                multiplier_for_shopping=1)
        return scores
