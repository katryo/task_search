# coding:utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class TaskGraphSimilarNodeFinder(AbstractTaskGraphManager):

    def similar_nodes_with_task_name(self, task_name):
        generalized_nodes = self.graph.successors(task_name)
        similar_nodes = set()
        for generalized_node in generalized_nodes:
            similar_nodes_per_g = self.graph.predecessors(generalized_node)
            for node in similar_nodes_per_g:
                similar_nodes.add(node)
        similar_nodes.discard(task_name)
        return similar_nodes
