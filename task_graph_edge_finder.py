# coding:utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from part_of_edge_finder_with_order import PartOfEdgeFinderWithOrder
import networkx
import pdb


class TaskGraphEdgeFinder(AbstractTaskGraphManager):

    def guess_original_with_task_name(self, task_name):
        aspects = self._aspects_with_task_name(task_name)
        for aspect in aspects:
            if aspect['is_original']:
                return True
        return False

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
        # results => [{'', '', ...}, {}, ...]
        results = self._same_url_nodes_with_task_name(task_name)
        for item in self._part_of_edges_by_entailment_with_task_name(task_name):
            results.append({item})
        return results

    def _same_url_nodes_with_task_name(self, task_name='query!!'):
        # 全ての関係がinstance-ofとかsubtype-ofだと過程しておいてから、
        # 「もしかしたら」part-ofなんじゃない？ と、
        # instance-of関係にあるっぽいエッジに訊ねる
        aspects = self._aspects_with_task_name(task_name)
        nodes = self.graph.nodes(data=True)
        results = []
        for aspect in aspects:
            if not aspect['is_original']:
                continue
            finder = PartOfEdgeFinderWithOrder(self_name=task_name, nodes=nodes, url=aspect['url'])
            name_shares_url = finder.task_name_shares_url()
            if name_shares_url:
                if not name_shares_url in results:
                    results.append(name_shares_url)
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
        if task_name in results:  # クエリタスク自身を省いている
            results.remove(task_name)
        return results

    def _subtype_of_edges_with_task_name(self, task_name):
        try:
            nodes = self.graph.predecessors(task_name)  # 特化
            nodes.extend(self.graph.successors(task_name))  # 汎化
            return set(nodes)  # task_name自身を含むことある
        except networkx.exception.NetworkXError:  # 検索クエリがtask_nameのときなど、ないこともある
            return set()

