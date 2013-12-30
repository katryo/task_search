# -*- coding: utf-8 -*-
import unittest
from sentence import Sentence
import pdb


class TestSentence(unittest.TestCase):

    def setUp(self):
        self.sentence_1 = Sentence('夏野菜へのシフトをスタートさせましょう')
        self.sentence_1.set_m_body_words_by_combine_nouns()

        self.sentence_2 = Sentence('クワなどは体格や体力に応じたものを、吟味して選ぶようにしましょう')
        self.sentence_2.set_m_body_words_by_combine_nouns()

    def test_includes_wo(self):
        result = self.sentence_1.includes_wo()
        self.assertEqual(result, True)

    def test_m_words_before_wo(self):
        m_words = self.sentence_1.m_words_before_wo()
        results = [m.name for m in m_words]
        self.assertEqual(results, ['夏野菜', 'へ', 'の', 'シフト'])

    def test_m_words_after_wo(self):
        m_words = self.sentence_1.m_words_after_wo()
        results = [m.name for m in m_words]
        self.assertEqual(results, ['スタート', 'さ', 'せ', 'ましょ', 'う'])

    def test_core_object(self):
        result = self.sentence_1.core_object()
        self.assertEqual(result, '夏野菜へのシフト')

        self.assertEqual(self.sentence_2.core_object(), 'もの')

    def test_core_verb(self):
        result = self.sentence_1.core_verb()
        self.assertEqual(result, 'スタートする')

        self.assertEqual(self.sentence_2.core_verb(), '選ぶ')

if __name__ == '__main__':
    unittest.main()
