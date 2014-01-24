#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from task_graph_edge_finder import TaskGraphEdgeFinder

class TaskGraphNodeSelector(AbstractTaskGraphManager):
    """
    検索結果表示に使う。
    1. すべての「良い」エッジを出す
    2. part-ofの同一階層にあるノードをまとめる
    3. subtype-ofにあるタスクは上位タスクにつなげる
    4. subtype-ofの親ノードと、他の良いノードとは関係のないノード、part-ofの汎化ノードのすべてをinstance-ofとして表示する。
    """

    def __init__(self, graph=False, query='部屋　掃除する'):
        super().__init__(graph)
        self.query_task = '_'.join(query.split('　'))
        self.subtype_of_tasks = set()
        self.part_of_task_clusters = []

    def first_result_tasks(self):
        results = dict()
        self.subtype_of_tasks = self._tasks_in_subtype_of_relation()
        self.part_of_task_clusters = self._task_clusters_in_part_of_relation()
        results['instance-of'] = []
        return results

    def _tasks_in_instance_if_relation(self):
        pass

    def _tasks_in_subtype_of_relation(self):
        # 最初のクエリ'部屋_掃除する'に対する'子供部屋_掃除する'のようなものを出力
        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_names = edge_finder.subtype_of_edges_lead_to_original_task_with_task_name(self.query_task)
        return task_names

    def _task_clusters_in_part_of_relation(self):
        edge_finder = TaskGraphEdgeFinder(self.graph)
        frequent_tasks = self._frequent_original_tasks()
        for subtype_of_task in self.subtype_of_tasks:
            frequent_tasks.remove(subtype_of_task)

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
                results.add(good_original_task)
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
        return results

