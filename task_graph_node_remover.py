# -*- coding: utf-8 -*-
from abstract_task_graph_manager import AbstractTaskGraphManager


class TaskGraphNodeRemover(AbstractTaskGraphManager):
    def remove_low_score_generalized_tasks(self):
        low_score_generalized_task_names = self._generalized_task_names_in_score_lower_than()
        self.graph.remove_nodes_from(low_score_generalized_task_names)
        print('削除したノードは以下の通りです')
        print(low_score_generalized_task_names)

    def _generalized_task_names_in_score_lower_than(self):
        task_names_lower_in_score = self._task_names_in_score_lower_than()
        results = set()
        for task_name in task_names_lower_in_score:
            aspects = self._aspects_with_task_name(task_name)
            is_original = False
            for aspect in aspects:
                if aspect['is_original']:
                    is_original = True
                    break
            if is_original:
                continue
            results.add(task_name)
        return results

    def _task_names_in_score_lower_than(self, num=2):
        scores = self.graph.in_degree()  # {'調味料_ばらまく': 1, ...}
        results = [name for name in scores if scores[name] < num]
        return results

    def _original_task_names_lead_to_higher_score_nodes(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        good_original_task_names = set()
        for generalized_task in task_names_with_higher_score:
            task_names = self.graph.predecessors(generalized_task)
            for task_name in task_names:
                good_original_task_names.add(task_name)
        return good_original_task_names

