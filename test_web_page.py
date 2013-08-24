import unittest
from web_page import WebPage
import pdb

class TestWebPage(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_lines_from_texts(self):
        result_xml_page = WebPage()
        f = open('swimming.xml')
        result_xml_page.xml_body = f.read()
        f.close()
        result_xml_page.pick_texts()
        # result_xml_page.result_pages => result_page
        for result_page in result_xml_page.result_pages:
            result_page.set_lines_from_texts()
            result_page.set_line_nums_with_word('上達')
            result_page.set_line_nums_around_action_word()
            result_page.set_line_clusters_around_action_word()
        for result_page in result_xml_page.result_pages:
            self.assertIn('上達', result_page.line_clusters_around_action_word[0][2])
        #TODO: テスト

    def test_set_clusters_around_action_word(self):
        result_page = WebPage()
        result_page.lines = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
        result_page.line_nums_around_action_word = set([0, 1, 3, 4, 5, 9, 10])
        result_page.set_line_clusters_around_action_word()
        self.assertEqual(result_page.line_clusters_around_action_word, [['a', 'b'], ['d', 'e', 'f'], ['j', 'k']])


    def test_set_line_nums_with_word(self):
        result_page = WebPage()
        result_page.lines = ['abc', 'bcd', 'cde']
        result_page.set_line_nums_with_word('b')
        self.assertEqual(result_page.line_nums_with_action_word, set([0, 1]))

    def test_set_line_nums_around_action_word(self):
        result_page = WebPage()
        result_page.lines = ['aa', 'bbbb', 'ccccc', 'ddddd', 'aaaaa', 'eeeee']
        result_page.set_line_nums_with_word('a')
        result_page.set_line_nums_around_action_word()
        self.assertEqual(result_page.line_nums_around_action_word, set([0, 1, 3, 4, 5]))

if __name__ == '__main__':
    unittest.main()