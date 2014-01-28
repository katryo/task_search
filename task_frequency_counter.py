#coding: utf-8


class TaskFrequencyCounter(object):
    """
    zeroのために作った
    """
    def __init__(self, nodes):
        self.nodes = nodes

    def original_task_scores(self):
        original_task_scores = dict()
        for node in self.nodes:
            try:
                aspects = node[1]['aspects']
                original_counter = 0
                for aspect in aspects:
                    if aspect['is_original'] is True:
                        original_counter += 1
                if original_counter > 0:
                    original_task_scores[node[0]] = original_counter
            except IndexError:
                continue
        return original_task_scores

    def frequency_with_task_name(self, task_name):
        node = self.nodes[task_name]
        aspects = node[1]['aspects']
        num_of_appearance = 0
        for aspect in aspects:
            if aspect['is_original']:
                num_of_appearance += 1
        return num_of_appearance
