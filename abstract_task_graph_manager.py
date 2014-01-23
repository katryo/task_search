import networkx as nx


class AbstractTaskGraphManager(object):
    def __init__(self, graph=False):
        self.graph = graph or nx.MultiDiGraph()
