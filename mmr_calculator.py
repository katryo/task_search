from sim_calculator import SimCalculator


class MMRCalculator(object):
    def __init__(self, graph, scores):
        self.graph = graph
        self.scores = scores
        self.i = 0  # mmrが呼ばれるたびに増える
        self.lambda_p = 0.5

    def mmr(self):
        cluster_score_pair = self._argmax()
        self.i += 1
        return cluster_score_pair

    def _argmax(self):


    def _left(self):
        return self.lambda_p * self._score(self.i)

    def _right(self):
        return (1 - self.lambda_p) * self._max_sim()

    def _max_sim(self):
        sim_calculator = SimCalculator(self.graph)







    def _score(self, index):
        return self.scores[index][1]