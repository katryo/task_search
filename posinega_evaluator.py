from m_words_factory import MWordsFactory
from takamura_data_loader import TakamuraDataLoader


class PosinegaEvaluator(object):
    def score_of_sentence(self, sentence):
        factory = MWordsFactory()
        m_words = factory.build_from(sentence)
        words = [m_word.name for m_word in m_words]
        sum_of_score = 0.0
        with TakamuraDataLoader() as loader:
            for word in words:
                score = loader.score_with_term(word)
                if score > 0.7:
                    sum_of_score += score
        return sum_of_score

if __name__ == '__main__':
    evaluator = PosinegaEvaluator()
    score = evaluator.score_of_sentence('山登りをしたせいか足が疲れた。苦しい。今日はゆっくり休みたい。あー眠いな。')
    print(score)