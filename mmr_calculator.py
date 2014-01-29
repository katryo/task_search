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
            if self._score_in_parenthesis(cluster_score_pair) > \
            self._score_in_parenthesis(max_cluster_score_pair):
                max_cluster_score_pair = cluster_score_pair

        return max_cluster_score_pair

    def _score_in_parenthesis(self, cluster_score_pair):
        return self._left() - self._right()


    def _left(self):
        return self.lambda_p * self._score(self.i)

    def _right(self):
        return (1 - self.lambda_p) * self._max_sim()

    def _max_sim(self):
        sim_calculator = SimCalculator(self.graph)
        max_sim = 0.0
        for selected in self.scores_selected:







    def _score(self, index):
        return self.scores[index][1]