from abstract_task_graph_manager import AbstractTaskGraphManager
import pdb
import constants


class SubtypeFinder(AbstractTaskGraphManager):
    def subtypes(self):
        subtype_nouns = self._subtype_nouns()
        # とりあえず名詞だけでok
        return subtype_nouns

    def _subtype_nouns(self):
        task_names = self.graph.nodes()
        subtype_nouns = set()
        for task_name in task_names:
            aspects = self._aspects_with_task_name(task_name)
            for aspect in aspects:
                dists = aspect['distance_between_subtypes']
                for dist in dists:
                    if dist in constants.STOPWORDS_OF_SUBTYPES:
                        continue
                    subtype_nouns.add(dist)
        return subtype_nouns


