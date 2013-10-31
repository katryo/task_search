# -*- coding: utf-8 -*-
import unittest
from web_page import WebPage
import pdb

class TestWebPage(unittest.TestCase):

    def setUp(self):
        self.nanapi_article_page = WebPage()
        nanapi_file = open('test_support/nanapi.html', encoding='utf-8')
        nanapi_html = nanapi_file.read()
        nanapi_file.close()
        self.nanapi_article_page.html_body = nanapi_html
        self.nanapi_article_page.url = 'http://nanapi.jp'

    def test_find_task_from_nanapi_with_headings(self):
        task = self.nanapi_article_page.find_task_from_nanapi_with_headings()
        self.assertEqual(task.title, '三万円以下で買えるハイテクアウターまとめ | nanapi [ナナピ]')
        self.assertEqual(task.url, 'http://nanapi.jp')
        self.assertEqual(task.steps[1].h2, '買う前に知っておきたい用語')
        self.assertEqual(task.steps[1].h3s[0], '耐水圧')
        self.assertEqual(task.steps[1].h3s[1], '透湿性')
        self.assertEqual(task.steps[1].h3s[2], 'DWR（Durable Water Repellent）')

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

    def test_build_header_tree(self):
        self.nanapi_article_page.fetch_html()
        self.nanapi_article_page.build_header_tree()

if __name__ == '__main__':
    unittest.main()