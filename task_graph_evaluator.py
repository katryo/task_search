from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class TaskGraphEvaluator(AbstractTaskGraphManager):
    def appearance_count_with_task_cluster(self, task_cluster):
        num_of_appearance = 0
        for task_name in task_cluster:
            aspects = self._aspects_with_task_name(task_name)
            num_of_appearance += len(aspects)
        return num_of_appearance
