# -*- coding: utf-8 -*-
import networkx as nx
import pdb
from hypohype_data_loader import HypoHypeDBDataLoader
from entailment_librarian import EntailmentLibrarian


class GraphTaskMapper():
    def __init__(self):
        self.graph = nx.DiGraph()

    def has_stop_object_term(self, object_term):
        stop_words = ['こと', 'もの', 'など']
        if object_term in stop_words:
            return True
        return False

    def _add_new_node(self, object_term, predicate_term, order):
        if self.has_stop_object_term(object_term):
            return False
        # orderは、1ページに1タスクなら0。順序があるなら、そのタスクも、上位タスクにもorderが与えられる。orderは1から始まる。
        self.graph.add_node('%s_%s' % (object_term, predicate_term), order=order)
            # オリジナルのノードから、上位・下位に貼る。自分自身にも貼っている。

    def _add_new_edge(self, task, noun, verb, entailment_type):
        if self.has_stop_object_term(noun):
            return False
        self.graph.add_edge('%s_%s' %
                            (task.object_term.name, task.predicate_term),
                            '%s_%s' %
                            (noun, verb),
                            entailment_type=entailment_type)

    def in_degree(self):
        return self.graph.in_degree()

    def add_node_and_edge_with_task(self, task):
        """
        もし1ページ内に順序があればorder=1から始まる値を与える。
        """
        nouns = self.hypes(task)
        nouns.append(task.object_term.name)
        verbs = self._entailing_preds(task)
        verbs['original'] = task.predicate_term

        # 上位語・下位語が揃った。
        for noun in nouns:
            for entailment_type in verbs:  # verbsはdict
                for verb in verbs[entailment_type]:
                    self._add_new_node(noun, verb, task.order)
                    self._add_new_edge(task, nouns, verb, entailment_type)

    def hypes(self, task):
    # object_term.core_nounのhypohypeを探る
        hhdbdl = HypoHypeDBDataLoader()
        hypes = hhdbdl.select_hypes_with_hypo(task.object_term.name)
        return hypes

    def _entailing_preds(self, task):
        librarian = EntailmentLibrarian()
        entailing_predicates = librarian.entailing_from_all_except_for_nonent_ntriv_with_entailed(task.predicate_term)
        return entailing_predicates  # dict

    def nodes_with_higher_in_degree_score(self):
        scores = self.in_degree()
        # ['機能_作る', '理念_よる']
        return [score for score in scores if scores[score] > 1]

    def broader_nodes_with_higher_in_degree_score(self):
        high_score_nodes = self.nodes_with_higher_in_degree_score()
        results = dict()
        for high_score_node in high_score_nodes:
            narrower_nodes = self.graph.predecessors(high_score_node)
            for narrower_node in narrower_nodes:
                if narrower_node.startswith('とき_'):
                    continue
                if narrower_node.startswith('など_'):
                    continue
                if narrower_node.startswith('こと_'):
                    continue
                if narrower_node.startswith('もの_'):
                    continue
                if high_score_node in results:
                    results[high_score_node].append(narrower_node)
                    continue
                results[high_score_node] = [narrower_node]
        return results  # dict型にする