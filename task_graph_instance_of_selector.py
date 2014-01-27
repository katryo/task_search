#coding: utf-8
from task_cluster import TaskCluster
from task_graph_edge_finder import TaskGraphEdgeFinder
from abstract_task_graph_manager import AbstractTaskGraphManager


class TaskGraphInstanceOfSelector(AbstractTaskGraphManager):
    def __init__(self,
                 graph=False,
                 candidate_tasks=set(),
                 subtype_of_tasks=set(),
                 part_of_tasks_clusters=set()):
        super().__init__(graph=graph)
        self.candidate_tasks = candidate_tasks
        self.subtype_of_tasks = subtype_of_tasks
        self.part_of_task_clusters = part_of_tasks_clusters

    def _tasks_in_instance_of_relation(self):
        task_names = self.candidate_tasks
        for subtype_of_task in self.subtype_of_tasks:
            task_names.remove(subtype_of_task)

        children_of_part_of_task_clusters = self._children_of_part_of_task_clusters()
        for child in children_of_part_of_task_clusters:
            try:
                task_names.remove(child)
            except KeyError:  # もうchildは削除されているとき
                continue
        return task_names

    def _children_of_part_of_task_clusters(self):
        children = set()
        for task_cluster in self.part_of_task_clusters:
            for task_name in task_cluster:
                children.add(task_name)
        return children

    def task_names_only_instance_of_with_task_names(self, task_names):
        task_names = self._task_names_excluded_subtype_of_with_task_names(task_names)
        task_names = self._task_names_excluded_part_of_with_task_names(task_names)
        return task_names


    def _task_names_excluded_subtype_of_with_task_names(self, task_names):
        for s_task_name in self.subtype_of_tasks:
            if s_task_name in task_names:
                task_names.remove(s_task_name)
        return task_names

    def _task_names_excluded_part_of_with_task_names(self, task_names):
        for cluster in self.part_of_task_clusters:
            for p_task_name in cluster:
                if p_task_name in task_names:
                    task_names.remove(p_task_name)
        return task_names
