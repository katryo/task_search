class TaskGraphEvaluator():
    def __init__(self, graph):
        self.graph = graph

    def _aspects_include_original(self, aspects):
        for aspect in aspects:
            if aspect['is_original']:
                return True
        return False

    def evaluate(self):
        for node in self.graph.nodes():
            edges = self.graph[node]
            for generalized_task in edges:
                entailment_type = edges[generalized_task].get('entailment_type')
                if entailment_type == 'nonent_predi' or entailment_type == 'ent_presu':
                    aspects = g.node[generalized_task]['aspects']
                    if self._aspects_include_original(aspects):
                        print('%s is a part-of %s because of entailment' % (node, generalized_task))
                        continue
                    print('%s is a part-of %s, but the later is not a original task' % (node, generalized_task))
                    # 次はorderでpart-ofを発見
                    # 貢献度があり、同じurlで、
                    # 汎化は1.頻度を調べて、2.part-of3subtype-ofを調べている。
                    # urlが同じであればそれはある上位タスク（おそらくクエリ）のpart-ofであることを意味する

                is_hype = edges[generalized_task].get('is_hype')
                if is_hype:
                    aspects = g.node[generalized_task]['aspects']
                    self._aspects_include_original(aspects)
                        print('%s is a subtype-of %s' % (node, generalized_task))
                        continue
                    print('%s is a subtype-of %s, but the later is not a original task' % (node, generalized_task))
