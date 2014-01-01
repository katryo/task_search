# -*- coding: utf-8 -*-
import unittest
from sentence import Sentence
from object_term import ObjectTerm
import pdb


class TestObjectTerm(unittest.TestCase):

    def setUp(self):
        self.ot = ObjectTerm('薬')

    def test_embodied_term_by_search(self):
        result_1 = self.ot.embodied_term_by_search('花粉症対策')
        self.assertIn('アレグラ', result_1)

if __name__ == '__main__':
    unittest.main()
