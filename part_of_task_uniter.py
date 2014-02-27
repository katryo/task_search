# coding: utf-8
from abstract_task_graph_manager import AbstractTaskGraphManager
from sim_calculator import SimCalculator
from task_graph_evaluator import TaskGraphEvaluator
import constants
import copy
import pdb


class PartOfTaskUniter(AbstractTaskGraphManager):
    """
    subtypeごとにまとめて、頻度と距離でフィルタリングする。
    1. そもそもタスク数の少ないsubtypeは除外すべき。
    なぜならノイズのsubtypeである可能性が高いから。
    しかし、どうせ最後のscore計算ではじかれる。
    2. frequencyの少ないタスクは除外すべき。ノイズの可能性が高い。
    3. 遠いタスクも除外すべき。
    4. ありふれすぎたタスクも、もういちど除外しては？
    """
    def __init__(self, graph=None, task_distance_pairs={'旅館': {('温泉_に_入る', 12), ('湯船_に_つかる', -4)}}):
        super().__init__(graph)
        self.task_distance_pairs = task_distance_pairs

    def unite(self):
        for subtype in self.task_distance_pairs:
            self._remove_far_tasks_with_subtype(subtype)
        return self.task_distance_pairs

    def _remove_far_tasks_with_subtype(self, subtype):
        pairs = copy.deepcopy(self.task_distance_pairs)
        for pair in pairs[subtype]:
            distance = pair[1]
            if distance > constants.THRESHOLD_DISTANCE_FOR_REMOVING_FROM_PART_OF:
                self.task_distance_pairs[subtype].remove(pair)
            if distance * 4 < - constants.THRESHOLD_DISTANCE_FOR_REMOVING_FROM_PART_OF:
                self.task_distance_pairs[subtype].remove(pair)

