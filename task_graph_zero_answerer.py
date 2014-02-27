from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from task_graph_part_of_selector_for_zero import TaskGraphPartOfSelectorForZero
from task_cluster_classifier_for_zero import TaskClusterClassifierForZero
from task_search_result_sorter import TaskSearchResultSorter
from part_of_task_scorer import PartOfTaskScorer
import pdb
import constants


class TaskGraphZeroAnswerer(AbstractTaskGraphAnswerer):
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph=graph, query_task=query_task)
        self.original_task_scores = self._original_task_scores()
        self.frequent_original_tasks = self._frequent_original_tasks()

    def set_task_scores(self):
        scorer = PartOfTaskScorer(self.graph)
        # self.part_of_task_clusters = {constants.SUPERTYPE_NAME: self.part_of_task_clusters}
        self.part_of_task_clusters_scores = scorer.scores(self.part_of_task_clusters)
        classifier = TaskClusterClassifierForZero(self.graph)
        #self.part_of_task_clusters_scores = classifier.task_name_frequency_pairs_with_part_of_task_clusters(self.part_of_task_clusters)
        self.instance_of_task_clusters_scores = classifier.task_name_frequency_pairs_with_instance_of_task_clusters(self.instance_of_task_clusters)

    def set_united_results(self):
        sorter = TaskSearchResultSorter(self)
        self.united_results = sorter.sorted_by_score()

#-------------initial setting-----
    def _original_task_scores(self):
        nodes = self.graph.nodes(data=True)
        scores = self._original_task_scores_with_nodes(nodes)
        return scores

    def _original_task_scores_with_nodes(self, nodes):
        original_task_scores = dict()
        for node in nodes:
            try:
                aspects = node[1]['aspects']
                original_counter = 0
                for aspect in aspects:
                    if aspect['is_original'] is True:
                        original_counter += 1
                if original_counter > 0:
                    original_task_scores[node[0]] = original_counter
            except IndexError:
                continue
        return original_task_scores

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

    def _task_clusters_in_part_of_relation(self):  # subのみのため
        task_names = self.frequent_original_tasks
        from task_graph_part_of_selector_for_first import TaskGraphPartOfSelectorForFirst
        from part_of_task_uniter import PartOfTaskUniter
        from same_url_part_of_task_uniter import SameURLPartOfTaskUniter

        selector = TaskGraphPartOfSelectorForFirst(self.graph,
                                                   candidate_tasks=task_names,
                                                   subtype_of_tasks=self.subtype_of_tasks)
        task_distance_pairs = selector.task_distance_pairs()
        # ここでuniteしない。というのは？ subtypeのとき。
        uniter = PartOfTaskUniter(graph=self.graph, task_distance_pairs=task_distance_pairs)
        task_clusters = uniter.unite()
        # return task_clusters
        task_clusters_by_same_url = selector.part_of_task_clusters_with_task_names(task_names)
        same_url_uniter = SameURLPartOfTaskUniter(graph=self.graph, task_distance_pairs=task_clusters_by_same_url)
        same_url_uniter.unite_recursively()
        task_clusters_for_supertype = same_url_uniter.task_distance_pairs
        task_clusters[constants.SUPERTYPE_NAME] = task_clusters_for_supertype[constants.SUPERTYPE_NAME]
        return task_clusters

    def __task_clusters_in_part_of_relation(self):  # 一時的に
        selector = TaskGraphPartOfSelectorForZero(self.graph,
                                                  candidate_tasks=self.frequent_original_tasks,
                                                  subtype_of_tasks=set())
        # task_clusters => [{'a_b', 'c_d', ...}]
        task_clusters = selector.part_of_task_clusters()
        return task_clusters

#---------------instance-of------------
    def _task_clusters_in_instance_of_relation(self):
        task_names = list(self.frequent_original_tasks.keys())
        for part_of_task_cluster in self.part_of_task_clusters:
            for part_of_task_name in part_of_task_cluster:
                if part_of_task_name in task_names:
                    task_names.remove(part_of_task_name)

        task_clusters = []
        for task_name in task_names:
            task_clusters.append({task_name})
        # keysを1 item setにすべきかも。
        return task_clusters
