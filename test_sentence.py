# -*- coding: utf-8 -*-
import unittest
from sentence import Sentence
import pdb


class TestSentence(unittest.TestCase):

    def setUp(self):
        self.sentence_1 = Sentence('夏野菜へのシフトをスタートさせましょう')
        self.sentence_2 = Sentence('クワなどは体格や体力に応じたものを、吟味して選ぶようにしましょう')
        self.sentence_3 = Sentence('トイレ掃除方法を、解説していきましょう')
        self.sentence_4 = Sentence('地面を掘り上げていきましょう')

        self.sentence_5 = Sentence('右に移動してください')

    def test_includes_cmp(self):
        result = self.sentence_5.includes_cmp()
        self.assertEqual(result, True)

    def test_set_m_body_words_by_combine_words(self):
        result = self.sentence_4.m_body_words[2].name
        self.assertEqual(result, '掘り上げ')


    def test_m_words_before_wo(self):
        m_words = self.sentence_1.m_words_before_cmp()
        results = [m.name for m in m_words]
        self.assertEqual(results, ['夏野菜'])

    def test_m_words_after_wo(self):
        m_words = self.sentence_1.m_words_after_cmp()
        results = [m.name for m in m_words]
        self.assertEqual(results, ['の', 'シフト', 'を', 'スタート', 'さ', 'せ', 'ましょ', 'う'])

    def test_core_object(self):
        result = self.sentence_1.core_object()
        self.assertEqual(result, '夏野菜')

        self.assertEqual(self.sentence_2.core_object(), '体力')
        self.assertEqual(self.sentence_3.core_object(), 'トイレ掃除方法')

    def test_core_verb(self):
        result = self.sentence_1.core_predicate()
        self.assertEqual(result, 'スタートする')

        self.assertEqual(self.sentence_2.core_predicate(), '応じる')
        self.assertEqual(self.sentence_3.core_predicate(), '解説する')

    def test_direction_i(self):
        result_1 = self.sentence_1.direction_r_i()
        self.assertEqual(result_1, 1)

    def test_includes_wo_before_direction(self):
        result_1 = self.sentence_1.includes_cmp_before_direction()
        self.assertEqual(result_1, True)

if __name__ == '__main__':
    unittest.main()
