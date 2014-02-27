#coding: utf-8
import pdb
import constants
from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from subtype_finder import SubtypeFinder
from task_cluster import TaskCluster
from task_cluster_classifier_for_first import TaskClusterClassifierForFirst
from task_graph_part_of_selector_for_first import TaskGraphPartOfSelectorForFirst
from task_graph_instance_of_selector import TaskGraphInstanceOfSelector
from part_of_task_uniter import PartOfTaskUniter
from task_search_result_sorter import TaskSearchResultSorter
from part_of_task_scorer import PartOfTaskScorer
from same_url_part_of_task_uniter import SameURLPartOfTaskUniter


class TaskGraphFirstAnswerer(AbstractTaskGraphAnswerer):
    """
    部分的に改良した手法と全部改良した手法
scores[0] => (TaskCluster(
    {'不動産業者_に_確認する', '確認_を_する',
     '掃除_を_する', '明細_を_貰う', '全体_を_拭く'}
), 5265.0, {'http://www.hikkoshi-tatsujin.com/arrangement/clean.html'})
    """
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph=graph, query_task=query_task)
        self.frequent_original_tasks = self._frequent_original_tasks()

    def set_task_scores(self):
        """
        subtypeをキーにしたdict
         '子ども部屋': {('工夫_を_する', -15), ('綺麗_に_する', 63), ('浴衣_を_楽しむ', 11), ('掃除_を_する', -46)}, '逸話': {('男心_を_尊重する', -34)}}
        """
        scorer = PartOfTaskScorer(self.graph)
        self.part_of_task_clusters_scores = scorer.scores(self.part_of_task_clusters)
        classifier = TaskClusterClassifierForFirst(self.graph)
        self.instance_of_task_clusters_scores = classifier.instance_of_task_clusters_higher(self.instance_of_task_clusters)

    def set_united_results(self):
        sorter = TaskSearchResultSorter(self)
        # self.united_results = sorter.sorted_by_mmr()
        self.united_results = sorter.sorted_by_score()

    def remove_generalized_tasks(self):
        """
        すべてのaspectsを探しても、is_originalなaspectがなかったとき
        """
        task_names = self.graph.nodes()
        for task_name in task_names:
            if self._finds_original_with_task_name(task_name):
                continue
            self.graph.remove_node(task_name)

    def _finds_original_with_task_name(self, task_name):
        aspects = self._aspects_with_task_name(task_name)
        for aspect in aspects:
            if aspect['is_original']:
                return True
        return False

#-------private----------
    def _frequent_original_tasks(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        results = set()
        for generalized_task in task_names_with_higher_score:
            good_original_task_names = self.graph.predecessors(generalized_task)
            good_original_tasks = []
            for task_name in good_original_task_names:
                task_attr_dict = self.graph.node[task_name]
                task_attr_dict['name'] = task_name
                good_original_tasks.append(task_attr_dict)

            # もうここにfreqを淹れればよいのでは
            for good_original_task in good_original_tasks:
                results.add(good_original_task['name'])
        return results

    def _task_names_in_score_higher_than(self, num=5):
        scores = self.graph.in_degree()  # {'調味料_ばらまく': 1, ...}
        results = [name for name in scores if scores[name] > num]
        return results  # original_taskはほとんどない。

#---------------subtype-of------------

    def _tasks_in_subtype_of_relation(self):
        # 最初のクエリ'部屋_掃除する'に対する'子供部屋_掃除する'のようなものを出力
        subtype_finder = SubtypeFinder(self.graph)
        task_nouns = subtype_finder.subtypes()
        return task_nouns

#---------------part-of------------
    def _task_clusters_in_part_of_relation(self):
        task_names = self.frequent_original_tasks
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


#---------------instance-of------------

    def _task_clusters_in_instance_of_relation(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        task_clusters = []  # [{'a_b', 'a_c', ...}]
        # ひとつでも共通するタスクがあればtask_clusterは貪欲にとりこんでいく
        for generalized_task in task_names_with_higher_score:
            good_original_task_names = self.graph.predecessors(generalized_task)
            if good_original_task_names:
                selector = TaskGraphInstanceOfSelector(graph=self.graph,
                                                       candidate_tasks=self.frequent_original_tasks,
                                                       subtype_of_tasks=self.subtype_of_tasks,
                                                       part_of_tasks_clusters=self.part_of_task_clusters)
                good_original_task_names = selector.task_names_only_instance_of_with_task_names(good_original_task_names)
                if good_original_task_names:
                    task_cluster = TaskCluster(good_original_task_names)
                    i_clusters = task_cluster.i_cluster_shares_task_with_clusters(task_clusters)
                    if i_clusters == -1:
                        task_clusters.append(task_cluster)
                        continue
                        # ここでTaskClusterオブジェクトではなくsetオブジェクトになる。
                    task_clusters[i_clusters] = TaskCluster(task_clusters[i_clusters].union(task_cluster))
        return task_clusters

