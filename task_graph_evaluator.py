from generalized_task import GeneralizedTask
from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class TaskGraphEvaluator(AbstractTaskGraphManager):
    def evaluate(self):
        for node in self.graph.nodes():
            edges = self.graph[node]
            for generalized_task_text in edges:
                edge = edges[generalized_task_text]
                generalized_task = GeneralizedTask(name=generalized_task_text,
                                                   edge=edge,
                                                   graph=self.graph,
                                                   original_task_name=node)
                generalized_task.print_part_of()  # エンテイルメント辞書で
                generalized_task.print_subtype_of()


