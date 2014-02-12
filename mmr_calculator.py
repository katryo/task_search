from sklearn.metrics import jaccard_similarity_score
import pdb


class MMRCalculator(object):
    def __init__(self, graph, scores):
        self.graph = graph
        self.scores_candidate = scores  # => [(TaskCluster({'a_b', 'c_d', ...}), 110), ...]
        self.scores_selected = []
        self.lambda_p = 0.5

    def mmr(self):
        cluster_score_pair = self._argmax()
        self.scores_selected.append(cluster_score_pair)
        try:
            self.scores_candidate.remove(cluster_score_pair)
        except ValueError:
            pass  # scoresが10ないときはここにくる
        return cluster_score_pair

    def _argmax(self):
        # scores_candidate => (({}, 111), 'PART-OF')
        try:
            max_cluster_score_pair_type_pair = self.scores_candidate[0]
        except IndexError:  # scoresが10個ないときもある
            return tuple([set(), 0, 'NONE'])
        for cluster_score_pair in self.scores_candidate:
            if self._score_in_square_bracket(cluster_score_pair) > \
               self._score_in_square_bracket(max_cluster_score_pair_type_pair):
                max_cluster_score_pair_type_pair = cluster_score_pair

        return max_cluster_score_pair_type_pair

    def _score_in_square_bracket(self, cluster_score_pair):
        return self._left(cluster_score_pair) - self._right(cluster_score_pair)

    def _left(self, cluster_score_pair):
        return self.lambda_p * cluster_score_pair[0][1]

    def _right(self, cluster):
        return (1 - self.lambda_p) * self._max_sim(cluster=cluster)

    def _max_sim(self, cluster):
        set_b = cluster[0][0]
        max_sim = 0.0
        for selected in self.scores_selected:
            set_a = selected[0][0]
            numerator = len(set_a.intersection(set_b))
            denominator = len(set_a.union(set_b))
            sim = numerator / denominator
            if sim >= max_sim:
                max_sim = sim
        return max_sim

    def _level_lists(self, list_a, list_b):
        diff = len(list_a) - len(list_b)
        if diff == 0:
            return list_a, list_b
        if diff > 0:
            for i in range(diff):
                list_b.append('')
            return list_a, list_b
        for i in range(-diff):
            list_a.append('')
        return list_a, list_b

