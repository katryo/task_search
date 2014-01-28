import math


class SimCalculator(object):
    def __init__(self, graph):
        self.graph = graph

    # a_set => {'夢_見つける', '未来_待つ'
    def similarity(self, a_set, b_set):
        # hypernimのhypornymリストにあれば


        a_set_nouns = []
        a_set_verbs = []
        b_set_nouns = []
        b_set_verbs = []
        for pair in a_set:
            words = pair.split('_')
            a_set_nouns.append(words[0])
            a_set_verbs.append(words[1])

        for pair in b_set:
            words = pair.split('_')
            b_set_nouns.append(words[0])
            b_set_verbs.append(words[1])


        result = self._cos()

    def _absolute(self, vector):
        # ベクトルvの長さつまり絶対値を返す
        squared_distance = sum([vector[word] ** 2 for word in vector])
        distance = math.sqrt(squared_distance)
        return distance

    def _cos(self, v1, v2):
        # v1 => {'a': 2, 'b': 3}
        numerator = 0
        # v1とv2で共通するkeyがあったとき、その値の積を加算していく。2つのベクトルの内積になる。
        for word in v1:
            if word in v2:
                numerator += v1[word] * v2[word]  # 回数

        denominator = self._absolute(v1) * self._absolute(v2)

        if denominator == 0:
            return 0
        return numerator / denominator

