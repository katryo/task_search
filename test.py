import unittest
from search_engine import SearchEngine
from web_page import WebPage
import pdb

class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_clueweb_search(self):
        se = SearchEngine()
        se.hint_word = '大学'
        se.action_word = '入学'
        se.set_solr_query()
        texts = se.clue_web_search(se.solr_query)
        self.assertEqual(len(texts), 50)
        self.assertEqual('大学' and '入学' in texts[0], True)

    def test_find_related_action_words_from_clueweb(self):
        se = SearchEngine()
        se.hint_word = '大学'
        se.action_word = '入学'
        se.set_solr_query()
        se.find_related_action_words_from_clueweb()
        self.assertEqual(se.result_pages, 10)

    def test_find_pages(self):
        page_1 = WebPage('http://tradein.nissan.co.jp/')
        page_1.title = '自動車の下取りと売却'
        page_1.snippet = '自動車には下取りをする方法がけっこうある。'

        page_2 = WebPage('http://www.link-nexus.com/')
        page_2.title = '自動車の下取りと販売'
        page_2.snippet = 'あばばばばば'

        page_3 = WebPage('http://toyota.jp/service/tradein/dc/top')
        page_3.title = '下取り参考価格情報'
        page_3.snippet = '下取りと販売ですよプロデューサーさん'

        search_engine = SearchEngine()
        search_engine.material_pages = [page_1, page_2, page_3]
        search_engine.hint_word = '自動車'
        search_engine.action_word = '下取り'
        search_engine.find_pages_including_related_words()
        self.assertEqual(search_engine.result_pages[0], page_1)
        self.assertEqual(search_engine.result_pages[1], page_2)
        self.assertEqual(search_engine.result_pages[2], page_3)

        search_engine.count_action_words()
        self.assertEqual(search_engine.action_words_count, {'販売': 2, '売却': 1})

        search_engine.sort_action_words_count()
        self.assertEqual(search_engine.sorted_action_words, [{'word': '販売', 'count': 2}, {'word': '売却', 'count': 1}])


if __name__ == '__main__':
    unittest.main()