import unittest
from ad import Ad
import pdb

class TestAd(unittest.TestCase):

    def setUp(self):
        pass

    def test_nara_phrase_normal(self):
        ad = Ad({'title': '健康を気にするなら', 'snippet': '夢ならたくさん見た', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        title_m_words = ad.to_m_words(ad.title)
        self.assertEqual(ad.till_three_words_before(title_m_words, 5), ['気', 'に', 'する'])

    def test_nara_phrase_after(self):
        ad = Ad({'title': '健康を気にするなら', 'snippet': '夢ならたくさん見た', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        title_m_words = ad.to_m_words(ad.title)
        self.assertEqual(ad.till_three_words_after(title_m_words, 5), [])

    def test_nara_phrase_before_is_in_the_beginning(self):
        ad = Ad({'title': '健康を気にするなら', 'snippet': '夢ならたくさん見た', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        snippet_m_words = ad.to_m_words(ad.snippet)
        self.assertEqual(ad.till_three_words_before(snippet_m_words, 1), ['夢'])

    def test_nara_phrase_after_is_in_the_beginning(self):
        ad = Ad({'title': '健康を気にするなら', 'snippet': '夢ならたくさん見た', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        snippet_m_words = ad.to_m_words(ad.snippet)
        self.assertEqual(ad.till_three_words_after(snippet_m_words, 1), ['たくさん', '見', 'た'])

    def test_de_phrase(self):
        ad = Ad({'title': '健康を気にするなら', 'snippet': '京アニでアニメを作ろう', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        snippet_m_words = ad.to_m_words(ad.snippet)
        self.assertEqual(ad.till_three_words_after(snippet_m_words, 2), ['アニメ', 'を', '作ろ'])

    def test_three_words_before_and_after(self):
        ad = Ad({'title': '健康を気にするなら', 'snippet': '京アニでアニメを作ろう', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        snippet_m_words = ad.to_m_words(ad.snippet)
        self.assertEqual(ad.till_three_words_after(snippet_m_words, 2), ['アニメ', 'を', '作ろ'])

if __name__ == '__main__':
    unittest.main()
