# -*- coding: utf-8 -*-
import unittest
from hypohype_data_loader import HypoHypeDBDataLoader
import pdb


class TestTaskStep(unittest.TestCase):

    def setUp(self):
        self.loader = HypoHypeDBDataLoader()

    def test_set_headings_from_text(self):
        hypes = self.loader.hypes_except_for_blockwords('家')
        expectation = ['名所', '建造物', '施設', '歴史的建造物', '町の施設']
        self.assertEqual(hypes, expectation)

if __name__ == '__main__':
    unittest.main()
