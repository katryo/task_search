# -*- coding: utf-8 -*-
import pdb
from hypohype_data_loader import HypoHypeDBDataLoader
from entailment_librarian import EntailmentLibrarian
from abstract_task_graph_manager import AbstractTaskGraphManager


class GraphTaskMapper(AbstractTaskGraphManager):
    def __init__(self, graph=None):
        super().__init__(graph)
        self.loader = HypoHypeDBDataLoader()

    def _add_new_node(self, object_term, predicate_term, order, url, is_original=False):
        if self._has_stop_object_term(object_term):
            return False

        task_name = '%s_%s' % (object_term, predicate_term)
        new_aspect = {
                'order': order,
                'url': url,
                'is_original': is_original
            }

        if task_name in self.graph.node:
            try:
                old_aspects = self._aspects_with_task_name(task_name)
                old_aspects.append(new_aspect)
                new_aspects = old_aspects
            except (KeyError, AttributeError):  # add_edgeでnodeが追加されたあと、nodeとして追加されたときに、ここに来る。
                new_aspects = [new_aspect]
        else:
            new_aspects = [new_aspect]
        self.graph.add_node(task_name, aspects=new_aspects)

    def _add_new_edge(self, task, noun, verb, entailment_type, is_hype):
        if self._has_stop_object_term(noun):
            return False
        if type(noun) == list or type(task.object_term.core_noun) == list:
            pdb.set_trace()
        self.graph.add_edge('%s_%s' %
                            (task.object_term.core_noun, task.predicate_term),
                            '%s_%s' %
                            (noun, verb),
                            entailment_type=entailment_type,
                            is_hype=is_hype)

    def _has_stop_object_term(self, object_term):
        stop_words = ['こと', 'もの', 'など']
        if object_term in stop_words:
            return True
        return False

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
        nouns['original'] = [original_noun]

        original_verb = task.predicate_term
        verbs = self._broader_preds(task)
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

                        if hype_type == 'hypes':
                            is_hype = True
                        else:
                            is_hype = False
                        self._add_new_edge(task=task,
                                           noun=noun,
                                           verb=verb,
                                           entailment_type=entailment_type,
                                           is_hype=is_hype)

    def _hypes(self, task):
        hypes = self.loader.hypes_except_for_blockwords(task.object_term.core_noun)
        return hypes

    def _broader_preds(self, task):
        librarian = EntailmentLibrarian()
        entailing_predicates = librarian.genaral_from_all_except_for_nonent_ntriv_with_special(task.predicate_term)
        return entailing_predicates  # dict

