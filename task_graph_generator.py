# -*- coding: utf-8 -*-
import pdb
from abstract_task_graph_manager import AbstractTaskGraphManager
import matplotlib.pyplot as plt
import networkx as nx


class TaskGraphGenerator(AbstractTaskGraphManager):

    def add_page(self, page):
        if page.subtypes:
            self._add_subtype_page(page)
        else:
            self._add_non_subtype_page(page)

    def _add_subtype_page(self, page):
        for subtype in page.subtypes:
            self.graph.add_edge(subtype, page.query_task(), relation='subtype-of')
            for task in page.tasks:
                pdb.set_trace()
                self.graph.add_edge(task.task_name(), subtype)

    def _add_non_subtype_page(self, page):
        for task in page.tasks:
            pdb.set_trace()
            self.graph.add_edge(task.task_name(), page.query_task())

    def show_graph(self):
        nx.draw(self.graph)
        plt.show()
        plt.savefig("path.png")


if __name__ == '__main__':
    import constants
    from pickle_file_loader_for_original import PickleFileLoaderForOriginal
    queries = constants.QUERIES_4
    for query in queries:
        generator = TaskGraphGenerator()
        pfl = PickleFileLoaderForOriginal()
        pages = pfl.load_fetched_pages_with_query(query)
        for i, page in enumerate(pages):
            if i > 100:
                break
            generator.add_page(page)
        generator.show_graph()
