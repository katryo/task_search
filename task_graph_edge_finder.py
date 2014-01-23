from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class TaskGraphEdgeFinder(AbstractTaskGraphManager):

    def part_of_edges_with_task_name(self, task_name):
        edges = self.graph.edge[task_name]
        results = set()
        for task_name_leaded_by_edge in edges:  # edgeはset()
            edges_dicts = edges[task_name_leaded_by_edge]
            for i in edges_dicts:
                edge_dict = edges_dicts[i]
                entailment_type = edge_dict['entailment_type']
                if entailment_type == 'nonentailment_predi' or entailment_type == 'entailment_presu':
                    results.add(task_name_leaded_by_edge)
        return results  # 先のノードのset

    def subtype_of_edges_with_task_name(self, task_name):
        edges = self.graph.edge[task_name]
        results = set()
        for task_name_leaded_by_edge in edges:  # edgeはset()
            edges_dicts = edges[task_name_leaded_by_edge]
            for i in edges_dicts:
                edge_dict = edges_dicts[i]
                if edge_dict['is_hype']:
                    results.add(task_name_leaded_by_edge)
        return results

