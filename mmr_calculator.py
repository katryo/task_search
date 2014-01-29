from sim_calculator import SimCalculator


class MMRCalculator(object):
    def __init__(self, graph, scores):
        self.graph = graph
        self.scores_candidate = scores  # => [(TaskCluster({'a_b', 'c_d', ...}), 110), ...]
        self.scores_selected = []
        self.lambda_p = 0.5

    def mmr(self):
        cluster_score_pair = self._argmax()
        self.scores_selected.append(cluster_score_pair)
        self.scores_candidate.remove(cluster_score_pair)
        return cluster_score_pair

    def _argmax(self):
        max_cluster_score_pair = self.scores_candidate[0]
        for cluster_score_pair in self.scores_candidate:
            if self._score_in_square_bracket(cluster_score_pair) > \
            self._score_in_square_bracket(max_cluster_score_pair):
                max_cluster_score_pair = cluster_score_pair

        return max_cluster_score_pair

    def _score_in_square_bracket(self, cluster_score_pair):
        return self._left(cluster_score_pair) - self._right(cluster_score_pair[0])

    def _left(self, cluster_score_pair):
        return self.lambda_p * cluster_score_pair[1]

    def _right(self, cluster):
        return (1 - self.lambda_p) * self._max_sim(set_b=cluster)

    def _max_sim(self, set_b):
        sim_calculator = SimCalculator(self.graph)
        max_sim = 0.0
        for selected in self.scores_selected:
            set_a = selected[0]
            sim = sim_calculator.similarity(set_a, set_b)
            if sim >= max_sim:
                max_sim = sim
        return max_sim








    def _score(self, index):
        return self.scores[index][1]