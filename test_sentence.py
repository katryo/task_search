# -*- coding: utf-8 -*-
import unittest
from sentence import Sentence
import pdb


class TestSentence(unittest.TestCase):

    def setUp(self):
        self.sentence_1 = Sentence('夏野菜へのシフトをスタートさせましょう', '')
        self.sentence_2 = Sentence('クワなどは体格や体力に応じたものを、吟味して選ぶようにしましょう', '')
        self.sentence_3 = Sentence('トイレ掃除方法を、解説していきましょう', '')
        self.sentence_4 = Sentence('地面を掘り上げていきましょう', '')
        self.sentence_5 = Sentence('右に移動してください', '')
        self.sentence_6 = Sentence('じっくり本を読む', '')
        self.sentence_7 = Sentence('水まわりは汚れやすいですから、定期的に掃除してガンコな汚れがつかないように気をつけておきましょう', '')

    def test_includes_cmp(self):
        result = self.sentence_5._cmp_r_i()
        self.assertEqual(result, 4)

    def test_set_m_body_words_by_combine_words(self):
        result = self.sentence_4.m_body_words[2].name
        self.assertEqual(result, '掘り上げ')


    def test_m_words_before_cmp(self):
        m_words = self.sentence_1._m_words_before_cmp()
        results = [m.name for m in m_words]
        self.assertEqual(results, ['夏野菜', 'へ', 'の', 'シフト'])

    def test_m_words_after_cmp(self):
        m_words = self.sentence_1.m_words_after_cmp()
        results = [m.name for m in m_words]
        self.assertEqual(results, ['スタート', 'さ', 'せ', 'ましょ', 'う'])

    def test_core_object(self):
        result = self.sentence_1._core_object()
        self.assertEqual(result, '夏野菜へのシフト')
        self.assertEqual(self.sentence_2._core_object(), 'もの')
        self.assertEqual(self.sentence_3._core_object(), 'トイレ掃除方法')
        self.assertEqual(self.sentence_6._core_object(), '本')
        self.assertEqual(self.sentence_7._core_object(), '')

    def test_core_predicate(self):
        result = self.sentence_1.core_predicate()
        self.assertEqual(result, 'スタートする')
        self.assertEqual(self.sentence_2.core_predicate(), '吟味する')
        self.assertEqual(self.sentence_3.core_predicate(), '解説する')
        self.assertEqual(self.sentence_6.core_predicate(), '読む')
        self.assertEqual(self.sentence_7.core_predicate(), '')

    def test_direction_i(self):
        result_1 = self.sentence_1.direction_r_i()
        self.assertEqual(result_1, 1)

if __name__ == '__main__':
    unittest.main()
