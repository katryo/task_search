#coding: utf-8
from task_frequency_counter import TaskFrequencyCounter
from abstract_task_cluster_classifier import AbstractTaskClusterClassifier
import pdb


class TaskClusterClassifierForZero(AbstractTaskClusterClassifier):
    def task_name_frequency_pairs_with_part_of_task_clusters(self, clusters):
        task_names_frequency_pairs = []
        node_dict = self.graph.node
        counter = TaskFrequencyCounter(node_dict)
        for cluster in clusters:
            num_of_appearance = 0
            for task_name in cluster:
                num_of_appearance += counter.frequency_with_task_name(task_name)
            task_names_frequency_pair = (cluster, num_of_appearance)
            task_names_frequency_pairs.append(task_names_frequency_pair)
        results = self._sorted_by_score(task_names_frequency_pairs)
        return results

    #---------instance_of---
    def task_name_frequency_pairs_with_instance_of_task_clusters(self, clusters):
        task_name_frequency_pairs = []
        node_dict = self.graph.node
        counter = TaskFrequencyCounter(node_dict)
        for cluster in clusters:
            for task_name in cluster:
                num_of_appearance = counter.frequency_with_task_name(task_name)
                task_name_frequency_pair = (set([task_name]), num_of_appearance)
                task_name_frequency_pairs.append(task_name_frequency_pair)
        results = self._sorted_by_score(task_name_frequency_pairs)
        return results

