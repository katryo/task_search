from abstract_task_graph_answerer import AbstractTaskGraphAnswerer
from task_graph_edge_finder import TaskGraphEdgeFinder


class task_graph_zero_answerera(AbstractTaskGraphAnswerer):
    def __init__(self, graph=False, query_task='部屋_掃除する'):
        super().__init__(graph=graph, query_task=query_task)
        self._set_original_tasks(self)

    def _tasks_in_subtype_of_relation(self):
        return set()

    def _task_clusters_in_part_of_relation(self):
        task_names = self.original_tasks

        edge_finder = TaskGraphEdgeFinder(self.graph)
        task_clusters = []  # [{'a_b', 'c_d'}, {e_f, 'g_h'}]
        # 高頻度の、subtypeでない、オリジナルのタスクの集合から、同じurlのものかentailment関係にあるものを見つける
        for task_name in self.original_tasks:
            task_names_list = edge_finder.part_of_edges_lead_to_original_node_with_task_name(task_name)

    def _set_original_tasks(self):
        self.original_tasks = self._original_tasks()

    def _original_tasks(self):
        nodes = self.graph.nodes(data=True)
        original_tasks = set()
        for node in nodes:
            try:
                if node[1]['is_original']:
                    original_tasks.add(node[0])
            except IndexError:
                continue
        return original_tasks