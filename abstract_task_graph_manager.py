# coding: utf-8
import networkx as nx
import pdb


class AbstractTaskGraphManager(object):
    def __init__(self, graph=None):
        self.graph = graph or nx.MultiDiGraph()

    def _aspects_with_task_name(self, task_name):
        try:
            aspects = self.graph.node[task_name]['aspects']
        except KeyError:
            return []
        if aspects is None:
            return []
        return aspects