#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from task_frequency_counter import TaskFrequencyCounter
import pdb


class TaskClusterClassifierForZero(AbstractTaskGraphManager):
    #---------part-of---
    def task_name_frequency_pairs_with_task_clusters(self, clusters):
        task_name_frequency_pairs = []
        node_dict = self.graph.node
        counter = TaskFrequencyCounter(node_dict)
        for cluster in clusters:
            for task_name in cluster:
                num_of_appearance = counter.frequency_with_task_name(task_name)
                task_name_frequency_pair = (task_name, num_of_appearance)
                task_name_frequency_pairs.append(task_name_frequency_pair)
        return task_name_frequency_pairs
