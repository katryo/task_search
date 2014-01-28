#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from task_frequency_counter import TaskFrequencyCounter


class TaskClusterClassifierForZero(AbstractTaskGraphManager):
    #---------part-of---
    def score_frequency_of_items_in_task_clusters(self, clusters):
        task_name_frequency_pairs = []
        nodes = self.graph.nodes(data=True)
        counter = TaskFrequencyCounter(nodes)
        for cluster in clusters:
            for task_name in cluster:
                num_of_appearance = counter.frequency_with_task_name(task_name)
                task_name_frequency_pair = (task_name, num_of_appearance)
                task_name_frequency_pairs.append(task_name_frequency_pair)
        return task_name_frequency_pairs
