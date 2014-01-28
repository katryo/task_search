from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from task_graph_part_of_selector_for_zero import TaskGraphPartOfSelectorForZero
from task_frequency_counter import TaskFrequencyCounter
from task_cluster_classifier_for_zero import TaskClusterClassifierForZero
import pdb


class TaskGraphZeroAnswerer(AbstractTaskGraphAnswerer):
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph=graph, query_task=query_task)
        self.original_task_scores = self._original_task_scores()
        self.frequent_original_tasks = self._frequent_original_tasks()

    def set_task_scores(self):
        classifier = TaskClusterClassifierForZero(self.graph)
        self.part_of_task_clusters_scores = classifier.score_frequency_of_items_in_task_clusters(self.part_of_task_clusters)
        self.instance_of_task_clusters_scores = classifier.score_frequency_of_items(self.instance_of_task_clusters)

#-------------initial setting-----
    def _original_task_scores(self):
        nodes = self.graph.nodes(data=True)
        counter = TaskFrequencyCounter(nodes)
        scores = counter.original_task_scores()
        return scores

    def _frequent_original_tasks(self):
        results = dict()
        for task_name in self.original_task_scores:
            if self.original_task_scores[task_name] > 1:
                results[task_name] = self.original_task_scores[task_name]
        return results

#---------------subtype-of------------
    def _tasks_in_subtype_of_relation(self):
        return set()

#---------------part-of------------

    def _task_clusters_in_part_of_relation(self):
        selector = TaskGraphPartOfSelectorForZero(self.graph,
                                                  candidate_tasks=self.frequent_original_tasks,
                                                  subtype_of_tasks=set())
        # task_clusters => [{'a_b', 'c_d', ...}]
        task_clusters = selector.part_of_task_clusters()
        return task_clusters

#---------------instance-of------------
    def _task_clusters_in_instance_of_relation(self):
        task_clusters = set(self.frequent_original_tasks.keys())
        # keysを1 item setにすべきかも。
        return task_clusters
