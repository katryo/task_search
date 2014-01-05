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

    def add_original_node(self, task):
        # まずオリジナルのノードを追加
        self.graph.add_node('%s_%s' % (task.object_term.name, task.predicate_term))
        # print('%s_%s' % (task.object_term.name, task.predicate_term))

    def hypes(self, task):
    # object_term.core_nounのhypohypeを探る
        sqldl = SQLiteDataLoader()
        hypes = sqldl.select_hypes_with_hypo(task.object_term.name)

    def entailing_preds(self, task):
        entailing_predicates = []
        for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
            if task.predicate_term in self.entailment_dictionaries[filename + '_entailing']:
                entailings = self.entailment_dictionaries[filename + '_entailing'][task.predicate_term]
                entailing_predicates.extend(list(entailings))

    def entailed_preds(self, task):
        entailed_predicates = []
        for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
            if task.predicate_term in self.entailment_dictionaries[filename + '_entailed']:
                entaileds = self.entailment_dictionaries[filename + '_entailed'][task.predicate_term]
                entailed_predicates.extend(list(entaileds))

    def add_new_node(self, object_term, predicate_term):
        g.add_node('%s_%s' % (object_term, predicate_term))
            # オリジナルのノードから、上位・下位に貼る。自分自身にも貼っている。

    def add_new_edge(self, task, object_term, predicate_term):
        g.add_edge('%s_%s' %
                   (task.object_term.name, task.predicate_term),
                   '%s_%s' %
                   (object_term, predicate_term))
