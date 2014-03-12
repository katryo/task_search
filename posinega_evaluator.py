#coding: utf-8
from m_words_factory import MWordsFactory
from evaluation_dict_data_loader import EvaluationDictDataLoader
import pdb


class PosinegaEvaluator(object):
    def __init__(self):
        with EvaluationDictDataLoader() as loader:
            positive_experiences_with_spaces = loader.positive_experiences()
            self.positive_experiences = [text.replace(' ', '') for text in positive_experiences_with_spaces]

    def score_of_sentence(self, sentence):
        factory = MWordsFactory()
        m_words = factory.build_from(sentence)
        stems = [m_word.stem for m_word in m_words]
        sum_of_score = 0.0
        stems_text = ''.join(stems)
        for positive_text in self.positive_experiences:
            if positive_text in stems_text:
                sum_of_score += 1
        return sum_of_score


if __name__ == '__main__':
    evaluator = PosinegaEvaluator()
    score = evaluator.score_of_sentence('とても嬉しいことがあった。気持ちがいい。')
    print(score)
    score = evaluator.score_of_sentence('aaa')
    print(score)
