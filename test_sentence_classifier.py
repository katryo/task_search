# -*- coding: utf-8 -*-
import unittest
from sentence import Sentence
from sentence_classifier import SentenceClassifier
import pdb


class TestSentenceClassifier(unittest.TestCase):

    def setUp(self):
        sentence_1 = Sentence('今すぐ泳ぎなさい')
        self.sc_1 = SentenceClassifier(sentence_1)

        sentence_2 = Sentence('魚雷を発射するとよい')
        self.sc_2 = SentenceClassifier(sentence_2)

        sentence_3 = Sentence('島風を育ててはいかがでしょう')
        self.sc_3 = SentenceClassifier(sentence_3)

        sentence_4 = Sentence('はい、大丈夫です！')
        self.sc_4 = SentenceClassifier(sentence_4)

    def test_cleared_one_hurdle_problem_i(self):
        result = self.sc_1.cleared_one_hurdle_problem_i()
        self.assertEqual(result, 3)

    def test_cleared_two_hurdle_problem_i(self):
        result = self.sc_2.cleared_two_hurdle_problem_i()
        self.assertEqual(result, 4)

        result_2 = self.sc_3.cleared_two_hurdle_problem_i()
        self.assertEqual(result_2, 3)

    def test_direction_i(self):
        result_1 = self.sc_1.direction_i()
        self.assertEqual(result_1, 3)
        result_2 = self.sc_2.direction_i()
        self.assertEqual(result_2, 4)
        result_3 = self.sc_3.direction_i()
        self.assertEqual(result_3, 3)
        result_4 = self.sc_4.direction_i()
        self.assertEqual(result_4, False)

if __name__ == '__main__':
    unittest.main()
