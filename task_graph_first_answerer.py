#coding: utf-8
import pdb
from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from task_graph_edge_finder import TaskGraphEdgeFinder
from task_cluster import TaskCluster
from task_graph_evaluator import TaskGraphEvaluator


class TaskGraphFirstAnswerer(AbstractTaskGraphAnswerer):
    """
    最初のタスク検索結果表示にだけ使う
    """
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph=graph, query_task=query_task)
        self._set_frequent_original_tasks()

    def _set_frequent_original_tasks(self):
        self.frequent_original_tasks = self._frequent_original_tasks()

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

    def _frequent_original_tasks_in_generalized_tasks(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        results = dict()
        for generalized_task in task_names_with_higher_score:
            good_original_task_names = self.graph.predecessors(generalized_task)
            good_original_tasks = []
            for task_name in good_original_task_names:
                task_attr_dict = self.graph.node[task_name]
                task_attr_dict['name'] = task_name
                good_original_tasks.append(task_attr_dict)

            # もうここにfreqを淹れればよいのでは
            results[generalized_task] = good_original_tasks  # 一見重複しているように見えるタスクかも
        return results  # {'調味料_まく': {name:'塩_ばらまく', url:'http...', 'order': 5 }}

    def _task_names_in_score_higher_than(self, num=1):
        scores = self.graph.in_degree()  # {'調味料_ばらまく': 1, ...}
        results = [name for name in scores if scores[name] > num]
        return results  # original_taskはほとんどない。

    def _tasks_in_subtype_of_relation(self):
        # 最初のクエリ'部屋_掃除する'に対する'子供部屋_掃除する'のようなものを出力
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_names = edge_finder.subtype_of_edges_lead_to_original_task_with_task_name(self.query_task)
        return task_names


    def _tasks_in_instance_of_relation(self):
        task_names = self.frequent_original_tasks
        for subtype_of_task in self.subtype_of_tasks:
            task_names.remove(subtype_of_task)

        children_of_part_of_task_clusters = self._children_of_part_of_task_clusters()
        for child in children_of_part_of_task_clusters:
            try:
                task_names.remove(child)
            except KeyError:  # もうchildは削除されているとき
                continue
        return task_names

    def _task_clusters_in_instance_of_relation(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        task_clusters = []  # [{'a_b', 'a_c', ...}]
        # ひとつでも共通するタスクがあればtask_clusterは貪欲にとりこんでいく
        for generalized_task in task_names_with_higher_score:
            good_original_task_names = self.graph.predecessors(generalized_task)
            if good_original_task_names:
                good_original_task_names = self._task_names_only_instance_of_with_task_names(good_original_task_names)
                if good_original_task_names:
                    task_cluster = TaskCluster(good_original_task_names)
                    i_clusters = task_cluster.i_cluster_shares_task_with_clusters(task_clusters)
                    if i_clusters == -1:
                        task_clusters.append(task_cluster)
                        continue
                    # ここでTaskClusterオブジェクトではなくsetオブジェクトになる。
                    task_clusters[i_clusters] = TaskCluster(task_clusters[i_clusters].union(task_cluster))
        return task_clusters

    def _task_names_only_instance_of_with_task_names(self, task_names):
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


    def _task_clusters_in_part_of_relation(self):
        edge_finder = TaskGraphEdgeFinder(self.graph)
        frequent_task_names = self._frequent_tasks_which_are_not_subtype_of()
        task_clusters = []  # [{'a_b', 'c_d'}, {e_f, 'g_h'}]
        for task_name in frequent_task_names:
            task_cluster = TaskCluster(edge_finder.part_of_edges_with_task_name(task_name))
            if task_cluster in task_clusters:  # 重複して数えているのを排除
                continue
            if task_cluster:
                if len(task_cluster) > 1:  # 1ページに1つだけタスク記述あるときはpart-ofでない
                    task_clusters.append(task_cluster)
        return task_clusters

    def _frequent_tasks_which_are_not_subtype_of(self):
        frequent_tasks = self.frequent_original_tasks
        for subtype_of_task in self.subtype_of_tasks:
            try:
                frequent_tasks.remove(subtype_of_task)
            except KeyError:  # subtype_of_taskがfrequentじゃないとき
                continue
        return frequent_tasks

    def set_selected_result_tasks(self):
        self.part_of_task_clusters_higher = self._part_of_task_clusters_higher()
        self.instance_of_task_clusters_higher = self._instance_of_task_clusters_higher()

    def _part_of_task_clusters_higher(self):
        results = []
        evaluator = TaskGraphEvaluator(self.graph)
        for cluster in self.part_of_task_clusters:
            result = (cluster, evaluator.contribution(cluster))
            results.append(result)
        results.sort(key=lambda result: result[1], reverse=True)
        return results

    def _instance_of_task_clusters_higher(self):
        results = []
        evaluator = TaskGraphEvaluator(self.graph)
        for cluster in self.instance_of_task_clusters:
            result = (cluster, evaluator.contribution(cluster))
            results.append(result)
        results.sort(key=lambda result: result[1], reverse=True)
        return results
