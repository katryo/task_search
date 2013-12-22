import unittest
import utils
import pdb

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.text_1 = 'あいう。えお！かきく。けこ'
        self.text_2 = 'あ？い?う。え？！お！かき？？く。けこ'
        self.text_list_1 = ['あいう。えお！かきく。けこ']

    def test_split_by_dots(self):
        result = utils.split_by_dots(self.text_1)
        expectation = ['あいう', 'えお', 'かきく', 'けこ']
        self.assertEqual(result, expectation)

    def test_split_by_dots_2(self):
        result = utils.split_by_dots(self.text_2)
        expectation = ['あ', 'い', 'う', 'え', 'お', 'かき', 'く', 'けこ']
        self.assertEqual(result, expectation)

    def test_split_and_flatten_by_a_certain_dot(self):
        result = utils.split_and_flatten_by_a_certain_dot(self.text_list_1, '。')
        expectation = ['あいう', 'えお！かきく', 'けこ']
        self.assertEqual(result, expectation)

if __name__ == '__main__':
    unittest.main()
