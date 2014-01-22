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

    def _add_new_node(self, object_term, predicate_term, order, url, is_original=False):
        if self.has_stop_object_term(object_term):
            return False
        if type(object_term) == list:
            pdb.set_trace()

        if '有料サービス' in object_term:
            if 'メールアドレス' in object_term:
                pdb.set_trace()
        # orderは、1ページに1タスクなら0。順序があるなら、そのタスクも、上位タスクにもorderが与えられる。orderは1から始まる。
        self.graph.add_node('%s_%s' % (object_term, predicate_term), order=order, url=url, is_original=is_original)
            # オリジナルのノードから、上位・下位に貼る。自分自身にも貼っている。

    def _add_new_edge(self, task, noun, verb, entailment_type, hype_type, from_original_task=False):
        if self.has_stop_object_term(noun):
            return False
        if type(noun) == list or type(task.object_term.core_noun) == list:
            pdb.set_trace()
        self.graph.add_edge('%s_%s' %
                            (task.object_term.core_noun, task.predicate_term),
                            '%s_%s' %
                            (noun, verb),
                            entailment_type=entailment_type,
                            hype_type=hype_type,
                            from_original_task=from_original_task)

    def in_degree(self):
        return self.graph.in_degree()

    def add_node_and_edge_with_task(self, task):
        """
        もし1ページ内に順序があればorder=1から始まる値を与える。
        """
        hypes = self._hypes(task)
        nouns = {'hypes': hypes}
        # hypesのときには、edgeにhypeエッジを与える必要ある？　subtype-ofを発見するために。
        original_noun = task.object_term.core_noun
        nouns['original'] = original_noun

        original_verb = task.predicate_term
        verbs = self._entailing_preds(task)
        verbs['original'] = tuple([original_verb])

        # 上位語・下位語が揃った。
        for hype_type in nouns:
            for noun in nouns[hype_type]:
                for entailment_type in verbs:  # verbsはdict
                    for verb in verbs[entailment_type]:
                        if noun == original_noun and verb == original_verb:
                            is_original = True
                        else:
                            is_original = False
                        self._add_new_node(object_term=noun,
                                           predicate_term=verb,
                                           order=task.order,
                                           url=task.url,
                                           is_original=is_original)
                        self._add_new_edge(task=task,
                                           noun=noun,
                                           verb=verb,
                                           entailment_type=entailment_type,
                                           hype_type=hype_type,
                                           from_original_task=is_original)

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
            if scores[generalized_task] < 2:
                continue
            good_original_task_names = self.graph.predecessors(generalized_task)
            good_original_tasks = []
            for task_name in good_original_task_names:
                task_attr_dict = self.graph.node[task_name]
                task_attr_dict['name'] = task_name
                good_original_tasks.append(task_attr_dict)

            results[generalized_task] = good_original_tasks  # 一見重複しているように見えるタスクかも
        return results  # {'調味料_まく': {name:'塩_ばらまく', url:'http...', 'order': 5 }}
