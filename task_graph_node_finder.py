from abstract_task_graph_manager import AbstractTaskGraphManager


class TaskGraphNodeFinder(AbstractTaskGraphManager):
    """
    直接使うことはなく、EdgeFinderから使われる。なぜなら、
    タスク検索はクエリノードのエッジを求めることから始まる。
    """
    # 同じgeneralized_taskにエッジを伸ばす2つのタスク。
    # これらを統合させる必要がある！ g_nodeの名前そのままではなく、
    # 重ね合わせ、集合体として。
    def frequent_original_tasks_by_generalized_tasks(self):
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

