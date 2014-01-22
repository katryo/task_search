from generalized_task import GeneralizedTask
import pdb


class TaskGraphEvaluator():
    def __init__(self, graph):
        self.graph = graph

    def evaluate(self):
        for node in self.graph.nodes():
            edges = self.graph[node]
            for generalized_task_text in edges:
                if generalized_task_text == '願_する':
                    pdb.set_trace()
                edge = edges[generalized_task_text]
                generalized_task = GeneralizedTask(name=generalized_task_text,
                                                   edge=edge,
                                                   graph=self.graph,
                                                   original_task_name=node)
                generalized_task.print_part_of()  # エンテイルメント辞書で
                generalized_task.print_subtype_of()


