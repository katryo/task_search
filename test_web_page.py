# -*- coding: utf-8 -*-
import unittest
import copy
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

        self.nanapi_hay_fever_page = WebPage('http://nanapi.jp')
        nanapi_hay_fever_file = open('test_support/nanapi_hay_fever.html', encoding='utf-8')
        nanapi_hay_fever_html = nanapi_hay_fever_file.read()
        nanapi_hay_fever_file.close()
        self.nanapi_hay_fever_page.html_body = nanapi_hay_fever_html

        self.gow_marriage_page = WebPage()
        gow_file = open('test_support/gow.html', encoding='utf-8')
        gow_html = gow_file.read()
        gow_file.close()
        self.gow_marriage_page.html_body = gow_html
        self.gow_marriage_page.url = 'http://magazine.gow.asia/love/column_details.php?column_uid=00000082'

        self.kanemoti_page = WebPage()
        kanemoti_file = open('test_support/kanemotilevel.html', encoding='utf-8')
        kanemoti_html = kanemoti_file.read()
        kanemoti_file.close()
        self.kanemoti_page.html_body = kanemoti_html

    def test_kanemoti_page(self):
        return None
        page = copy.deepcopy(self.kanemoti_page)
        page.build_heading_tree()
        self.assertEqual(page.top_nodes[0].heading_title, '耐水圧')


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
        return None
        page = copy.deepcopy(self.nanapi_article_page)
        page.build_heading_tree()
        self.assertEqual(page.top_nodes[0].children[0].heading_title, '買う前に知っておきたい用語')
        self.assertEqual(page.top_nodes[0].children[0].children[0].heading_title, '耐水圧')
        self.assertEqual(page.top_nodes[0].children[0].children[1].heading_title, '透湿性')
        self.assertEqual(page.top_nodes[0].children[0].children[3].heading_title, 'ベンチレーションポケット')

    def test_nanapi_hay_fever_page_build_heading_tree(self):
        page = self.nanapi_hay_fever_page
        page.build_heading_tree()
        #self.assertEqual(page.top_nodes[0].children[0].heading_title, '花粉が多く飛ぶ日')

    def test_slice_after_dots(self):
        page = WebPage()
        sentence_with_dots = 'あいうえお、かきくけこさしすせそ'
        result = page.slice_after_dots(sentence_with_dots)
        self.assertEqual(result, 'かきくけこさしすせそ')

        sentence_with_dots_2 = 'あいうえお、かきくけこ、さしすせそ'
        result = page.slice_after_dots(sentence_with_dots_2)
        self.assertEqual(result, 'さしすせそ')

        sentence_with_dots_3 = 'あいうえお、かきくけこ。さしすせそ'
        result = page.slice_after_dots(sentence_with_dots_3)
        self.assertEqual(result, 'さしすせそ')

        sentence_with_dots_4 = 'あいうえお。かきくけこ、さしすせそ'
        result = page.slice_after_dots(sentence_with_dots_4)
        self.assertEqual(result, 'さしすせそ')

    def test_combine_nouns(self):
        page = WebPage()
        m_words = page.to_m_words('親子決戦試合')
        results = page.combine_nouns(m_words)
        self.assertEqual(results[0].name, '親子決戦試合')

        m_words = page.to_m_words('そして勝敗決定戦に')
        results = page.combine_nouns(m_words)
        self.assertEqual(results[1].name, '勝敗決定戦')

    def test_combine_to_one_noun(self):
        page = WebPage()
        m_words = page.to_m_words('親子決戦')
        m_words_after_combine = page.combine_to_one_noun(m_words, 0)
        self.assertEqual(m_words_after_combine[0].name, '親子決戦')

    def test_prepare_task_sentence(self):
        page = WebPage()
        string = 'そこで「最強無敵魔法少女」になりました'
        m_words = page.prepare_task_sentence(string)
        self.assertEqual(m_words[0].name, 'そこで')
        self.assertEqual(m_words[1].name, '最強無敵魔法少女')
        self.assertEqual(m_words[2].name, 'に')
        self.assertEqual(m_words[3].name, 'なり')
        self.assertEqual(m_words[4].name, 'まし')
        self.assertEqual(m_words[5].name, 'た')

    def test_keyword_from_text(self):
        page = WebPage()
        string = 'しかしこの市販の薬を飲んで'
        task = page.from_suspicious_string_to_task_sentence(string)
        self.assertEqual(task, '市販の薬を飲んで')

        string = '医師や薬剤師は薬を飲まずに風邪を治す'
        task = page.from_suspicious_string_to_task_sentence(string)
        self.assertEqual(task, '薬を飲まずに風邪を治す')

if __name__ == '__main__':
    unittest.main()