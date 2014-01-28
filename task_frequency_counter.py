#coding: utf-8
import pdb


class TaskFrequencyCounter(object):
    """
    zeroのために作った
    """
    def __init__(self, node_dict):
        self.node_dict = node_dict

    def frequency_with_task_name(self, task_name):
        node = self.node_dict[task_name]
        aspects = node['aspects']
        num_of_appearance = 0
        for aspect in aspects:
            if aspect['is_original']:
                num_of_appearance += 1
        return num_of_appearance
