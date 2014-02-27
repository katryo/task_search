# -*- coding: utf-8 -*-
import pdb
from abstract_task_graph_manager import AbstractTaskGraphManager


class TaskGraphGenerator(AbstractTaskGraphManager):

    def add_page(self, page):
        if page.is_subtype():
            self._add_subtype_page(page)
        else:
            self._add_non_subtype_page(page)

    def _add_subtype_page(self, page):
        for subtype in page.subtypes:
            self.graph.add_edge(subtype, page.query_task(), relation='subtype-of')
            for task in page.tasks:
                self.graph.add_edge(task.task_name(), subtype)

    def _add_non_subtype_page(self, page):
        for task in page.tasks:
            self.graph.add_edge(task.task_name(), page.query_task())
