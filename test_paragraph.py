# -*- coding: utf-8 -*-
import unittest
from paragraph import Paragraph
import pdb


class TestParagraph(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        sentence = '/>あいうえお'
        p = Paragraph(sentence)
        self.assertEqual(p.sentences, ['あいうえお'])

        sentence = 'あいうえお<a href="somewhere">かき</a>くけこ'
        p = Paragraph(sentence)
        self.assertEqual(p.sentences, ['あいうえおかきくけこ'])

    def test_split_by_dots(self):
        p = Paragraph('a')

        html_items = p.split_by_dots('abc')
        self.assertEqual(html_items, ['abc'])

        html_items2 = p.split_by_dots('a.bc')
        self.assertEqual(html_items2, ['a', 'bc'])

        html_items2 = p.split_by_dots('a。bc')
        self.assertEqual(html_items2, ['a', 'bc'])

if __name__ == '__main__':
    unittest.main()