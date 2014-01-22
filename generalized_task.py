class GeneralizedTask(object):
    def __init__(self, name, edge, graph, original_task_name):
        self.name = name
        self.edge = edge
        self.graph = graph
        self.aspects = self.graph.node[self.name]['aspects']
        self.entailment_type = self.edge.get('entailment_type')
        self.original_task_name = original_task_name

    def print_part_of(self):
        if self._is_presu_like():
            if self._aspects_include_original():
                print('%s is a part-of %s because of entailment' % (self.edge[0], self.name))
            print('%s is a part-of %s, but the later is not a original task' % (self.edge[0], self.name))

    def _aspects_include_original(self):
        for aspect in self.aspects:
            if aspect['is_original']:
                return True
        return False

    def _is_presu_like(self):
        if self.entailment_type == 'nonent_predi':
            return True
        if self.entailment_type == 'ent_presu':
            return True
        return False

    def _is_hype(self):
        return self.edge.get('is_hype')

    def print_subtype_of(self):
        if self._is_hype:
            if self._aspects_include_original():
                print('%s is a subtype-of %s' % (self.original_task_name, self.name))
                return
            print('%s is a subtype-of %s, but the later is not a original task' % (self.original_task_name, self.name))
