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
        if type(object_term) == list:
            pdb.set_trace()

        if '有料サービス' in object_term:
            if 'メールアドレス' in object_term:
                pdb.set_trace()
        # orderは、1ページに1タスクなら0。順序があるなら、そのタスクも、上位タスクにもorderが与えられる。orderは1から始まる。
        self.graph.add_node('%s_%s' % (object_term, predicate_term), order=order)
            # オリジナルのノードから、上位・下位に貼る。自分自身にも貼っている。

    def _add_new_edge(self, task, noun, verb, entailment_type):
        if self.has_stop_object_term(noun):
            return False
        if type(noun) == list or type(task.object_term.core_noun) == list:
            pdb.set_trace()
        self.graph.add_edge('%s_%s' %
                            (task.object_term.core_noun, task.predicate_term),
                            '%s_%s' %
                            (noun, verb),
                            entailment_type=entailment_type)

    def in_degree(self):
        return self.graph.in_degree()

    def add_node_and_edge_with_task(self, task):
        """
        もし1ページ内に順序があればorder=1から始まる値を与える。
        """
        nouns = self._hypes(task)
        # hypesのときには、edgeにhypeエッジを与える必要ある？　subtype-ofを発見するために。
        nouns.append(task.object_term.core_noun)
        verbs = self._entailing_preds(task)
        verbs['original'] = tuple([task.predicate_term])

        # 上位語・下位語が揃った。
        for noun in nouns:
            for entailment_type in verbs:  # verbsはdict
                for verb in verbs[entailment_type]:
                    self._add_new_node(noun, verb, task.order)
                    self._add_new_edge(task, noun, verb, entailment_type)

    def _hypes(self, task):
    # object_term.core_nounのhypohypeを探る
        hhdbdl = HypoHypeDBDataLoader()
        hypes = hhdbdl.hypes_except_for_blockwords(task.object_term.core_noun)
        return hypes

    def _entailing_preds(self, task):
        librarian = EntailmentLibrarian()
        entailing_predicates = librarian.entailing_from_all_except_for_nonent_ntriv_with_entailed(task.predicate_term)
        return entailing_predicates  # dict

    def frequent_tasks_by_generalized_tasks(self):
        scores = self.in_degree()  # {'調味料_ばらまく': 1, ...}
        results = dict()
        for generalized_task in scores:
            if scores[generalized_task] < 1:
                continue
            good_original_tasks = self.graph.predecessors(generalized_task)
            results[generalized_task] = good_original_tasks  # 一見重複しているように見えるタスクかも
        return results  # dict
