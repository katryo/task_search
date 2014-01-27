#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager


class AbstractTaskGraphPartOfSelector(AbstractTaskGraphManager):
    def __init__(self,
                 graph=False,
                 candidate_tasks=set(),
                 subtype_of_tasks=set()):
        super().__init__(graph=graph)
        self.candidate_tasks = candidate_tasks
        self.subtype_of_tasks = subtype_of_tasks


#-------first--------

    # オリジナルの、高頻度のタスクだけ返す
    def _frequent_tasks_which_are_not_subtype_of(self):
        pass

    def _part_of_task_clusters_with_task_names(self, task_names):
        pass
