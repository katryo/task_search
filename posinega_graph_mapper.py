# -*- coding: utf-8 -*-
import pdb
from hypohype_data_loader import HypoHypeDBDataLoader
from entailment_librarian import EntailmentLibrarian
from abstract_task_graph_manager import AbstractTaskGraphManager


class PosinegaGraphMapper(AbstractTaskGraphManager):
    def __init__(self, graph=None):
        super().__init__(graph)
        self.loader = HypoHypeDBDataLoader()

    def add_edges_with_page(self, page):
        """
        もし1ページ内に順序があればorder=1から始まる値を与える。
        """
        if page.subtypes:
            for subtype in page.subtypes:
                self.graph.add_edge(page.query, subtype)
                self.graph.add_edge(subtype, page.url)
        else:
            self.graph.add_edge(page.query, page.url)

        for task in page.tasks:
            #if task.is_noise():
            #    continue
            self.graph.add_edge(page.url, '%s_%s_%s' % (task.object_term.core_noun, task.cmp, task.predicate_term))

    def in_degree(self):
        return self.graph.in_degree()

    def _hypes(self, task):
        hypes = self.loader.hypes_except_for_blockwords(task.object_term.core_noun)
        return hypes

    def _broader_preds(self, task):
        librarian = EntailmentLibrarian()
        entailing_predicates = librarian.genaral_from_all_except_for_nonent_ntriv_with_special(task.predicate_term)
        return entailing_predicates  # dict

