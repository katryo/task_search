#coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class AbstractTaskClusterClassifier(AbstractTaskGraphManager):
    def _sorted_by_score(self, pairs):
        pairs.sort(key=lambda result: result[1], reverse=True)
        return pairs

