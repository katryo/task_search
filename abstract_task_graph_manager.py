import networkx as nx


class AbstractTaskGraphManager(object):
    def __init__(self, graph=False):
        self.graph = graph or nx.MultiDiGraph()

    def _aspects_with_task_name(self, task_name):
        aspects = self.graph.node[task_name]['aspects']
        if aspects is None:
            return []
        return aspects