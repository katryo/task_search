from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb


class SubtypeFinder(AbstractTaskGraphManager):
    def subtypes(self):
        task_names = self.graph.nodes()
        subtype_names = set()
        for task_name in task_names:
            aspects = self._aspects_with_task_name(task_name)
            for aspect in aspects:
                dists = aspect['distance_between_subtypes']
                for dist in dists:
                    subtype_names.add(dist)
        pdb.set_trace()
        return subtype_names


