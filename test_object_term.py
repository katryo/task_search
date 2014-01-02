# -*- coding: utf-8 -*-
import unittest
from sentence import Sentence
from object_term import ObjectTerm
import pdb


class TestObjectTerm(unittest.TestCase):

    def setUp(self):
        self.ot = ObjectTerm(text='医師の診断', context='治療')

    def test_set_core_noun_from_name(self):
        self.ot.set_core_noun_from_name()
        self.assertEqual(self.ot.core_noun, '診断')

if __name__ == '__main__':
    unittest.main()
