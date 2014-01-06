# -*- coding: utf-8 -*-
import networkx as nx
import pdb
import utils
from sqlite_data_loader import SQLiteDataLoader
import constants


class GraphTaskMapper():
    def __init__(self):
        self.graph = nx.DiGraph()
        self.entailment_dictionaries = utils.load_entailment_dictionaries()

    def hypes(self, task):
    # object_term.core_nounのhypohypeを探る
        sqldl = SQLiteDataLoader()
        hypes = sqldl.select_hypes_with_hypo(task.object_term.name)
        return hypes

    def entailing_preds(self, task):
        entailing_predicates = []
        for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
            if task.predicate_term in self.entailment_dictionaries[filename + '_entailing']:
                entailings = self.entailment_dictionaries[filename + '_entailing'][task.predicate_term]
                entailing_predicates.extend(list(entailings))
        return entailing_predicates

    def entailed_preds(self, task):
        entailed_predicates = []
        for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
            if task.predicate_term in self.entailment_dictionaries[filename + '_entailed']:
                entaileds = self.entailment_dictionaries[filename + '_entailed'][task.predicate_term]
                entailed_predicates.extend(list(entaileds))
        return entailed_predicates

    def has_stop_object_term(self, object_term):
        stop_words = ['こと', 'もの', 'など']
        if object_term in stop_words:
            return True
        return False

    def add_new_node(self, object_term, predicate_term):
        if self.has_stop_object_term(object_term):
            return False
        self.graph.add_node('%s_%s' % (object_term, predicate_term))
            # オリジナルのノードから、上位・下位に貼る。自分自身にも貼っている。

    def add_new_edge(self, task, object_term, predicate_term):
        if self.has_stop_object_term(object_term):
            return False
        self.graph.add_edge('%s_%s' %
                            (task.object_term.name, task.predicate_term),
                            '%s_%s' %
                            (object_term, predicate_term))

    def in_degree(self):
        return self.graph.in_degree()

    def add_node_and_edge_with_task(self, task):
        hypes = self.hypes(task)
        entailing_predicates = self.entailing_preds(task)
        entailed_predicates = self.entailed_preds(task)

        # 上位語・下位語が揃った。
        for hype_or_original in (hypes + [task.object_term.name]):
            for entailing_or_entailed_or_original in (entailing_predicates +
                                                      entailed_predicates +
                                                      [task.predicate_term]):
                self.add_new_node(hype_or_original, entailing_or_entailed_or_original)
                self.add_new_edge(task, hype_or_original, entailing_or_entailed_or_original)
        #narrower_nodes = self.graph.predecessors('女性語_くしゃみ連発する')
        #if 'こと_忘れる' in narrower_nodes:
        #    pdb.set_trace()

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