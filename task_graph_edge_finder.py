from abstract_task_graph_manager import AbstractTaskGraphManager
from part_of_edge_finder_with_order import PartOfEdgeFinderWithOrder
import pdb


class TaskGraphEdgeFinder(AbstractTaskGraphManager):

    def part_of_edges_lead_to_original_node_with_task_name(self, task_name):
        task_names = self.part_of_edges_with_task_name(task_name)
        results = self._select_original_task_with_task_names(task_names)
        return results

    def _select_original_task_with_task_names(self, task_names):
        results = set()
        for _task_name in task_names:
            aspects = self._aspects_with_task_name(_task_name)
            for aspect in aspects:
                if aspect['is_original']:
                    results.add(_task_name)
        return results

    # 高スコアの汎化タスクも取ってくる。普段はlead_to_original_nodeを使うべき
    def part_of_edges_with_task_name(self, task_name):
        results = self._part_of_edges_by_order_with_task_name(task_name)
        for item in self._part_of_edges_by_entailment_with_task_name(task_name):
            results.add(item)
        return results

    def _part_of_edges_by_order_with_task_name(self, task_name='query!!'):
        # 全ての関係がinstance-ofとかsubtype-ofだと過程しておいてから、
        # 「もしかしたら」part-ofなんじゃない？ と、
        # instance-of関係にあるっぽいエッジに訊ねる
        aspects = self._aspects_with_task_name(task_name)

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
                e_type = edge_dict['entailment_type']
                if e_type == 'nonentailment_predi' or e_type == 'entailment_presu':
                    results.add(task_name_leaded_by_edge)
        return results  # 先のノードのset

    def subtype_of_edges_lead_to_original_task_with_task_name(self, task_name):
        task_names = self._subtype_of_edges_with_task_name(task_name)
        results = self._select_original_task_with_task_names(task_names)
        return results

    def _subtype_of_edges_with_task_name(self, task_name):
        try:
            edges = self.graph.edge[task_name]
        except KeyError:  # 検索クエリがtask_nameのときなど、ないこともある
            return set()
        results = set()
        for task_name_leaded_by_edge in edges:  # edgeはset()
            edges_dicts = edges[task_name_leaded_by_edge]
            for i in edges_dicts:
                edge_dict = edges_dicts[i]
                if edge_dict['is_hype']:
                    results.add(task_name_leaded_by_edge)
        return results

