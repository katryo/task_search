from abstract_task_graph_manager import AbstractTaskGraphManager
from part_of_edge_finder_with_order import PartOfEdgeFinderWithOrder
import pdb


class TaskGraphEdgeFinder(AbstractTaskGraphManager):

    def part_of_edges_with_task_name(self, task_name):
        results = self._part_of_edges_by_order_with_task_name()
        for item in self._part_of_edges_by_entailment_with_task_name():
            results.add(item)
        return results

    def _part_of_edges_by_order_with_task_name(self, task_name='query!!'):
        # 全ての関係がinstance-ofとかsubtype-ofだと過程しておいてから、
        # 「もしかしたら」part-ofなんじゃない？ と、
        # instance-of関係にあるっぽいエッジに訊ねる
        aspects = self.graph.node[task_name]['aspects']
        if aspects is None:
            return

        nodes = self.graph.nodes(data=True)
        results = set()
        for aspect in aspects:
            finder = PartOfEdgeFinderWithOrder(self_name=task_name, nodes=nodes, aspect=aspect)
            name_shares_url = finder.task_name_shares_url()
            if name_shares_url:
                results.add(name_shares_url)
        return results

    def _part_of_edges_by_entailment_with_task_name(self, task_name):
        edges = self.graph.edge[task_name]
        results = set()
        for task_name_leaded_by_edge in edges:  # edgeはset()
            edges_dicts = edges[task_name_leaded_by_edge]
            for i in edges_dicts:
                edge_dict = edges_dicts[i]
                entailment_type = edge_dict['entailment_type']
                # nonentailment_prediは違う気がする
                if entailment_type == 'entailment_presu':
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

