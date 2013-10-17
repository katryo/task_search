import unittest
from ad import Ad
import pdb

class TestAd(unittest.TestCase):

    def setUp(self):
        self.kyokuto_anime_snippet_ad = Ad({'title': 'a', 'snippet': '極東アニメーションで素敵な作品を描こう', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        self.chuni_snippet_ad = Ad({'title': 'a', 'snippet': '夢ならたくさん見た', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        self.health_title_ad = Ad({'title': '健康を気にするなら', 'snippet': 's', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        self.trigger_snippet_ad = Ad({'title': 'TRIGGERのキルラキルでアニメの新世界を見よう。あの今石洋之なら世界を変えられる！', 'snippet': 'TRIGGERのキルラキルでアニメの新世界を見よう。あの今石洋之なら世界を変えられる！', 'link': 'http://www.pref.nara.jp/item/83513.htm'})

    def test_nara_phrase_normal(self):
        ad = self.health_title_ad
        title_m_words = ad.to_m_words(ad.title)
        self.assertEqual(ad.till_three_words_before(title_m_words, 5), ['気', 'に', 'する'])

    def test_nara_phrase_after(self):
        ad = self.health_title_ad
        title_m_words = ad.to_m_words(ad.title)
        self.assertEqual(ad.till_three_words_after(title_m_words, 5), [])

    def test_nara_phrase_before_is_in_the_beginning(self):
        ad = self.chuni_snippet_ad
        snippet_m_words = ad.to_m_words(ad.snippet)
        self.assertEqual(ad.till_three_words_before(snippet_m_words, 1), ['夢'])

    def test_nara_phrase_after_is_in_the_beginning(self):
        ad = self.chuni_snippet_ad
        snippet_m_words = ad.to_m_words(ad.snippet)
        self.assertEqual(ad.till_three_words_after(snippet_m_words, 1), ['たくさん', '見', 'た'])

    def test_de_phrase(self):
        ad = self.kyokuto_anime_snippet_ad
        snippet_m_words = ad.to_m_words(ad.snippet)
        self.assertEqual(ad.till_three_words_after(snippet_m_words, 2), ['素敵', 'な', '作品'])

    def test_get_3_words_before_and_after(self):
        ad = self.kyokuto_anime_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        before_and_after = ad.get_3_words_before_and_after(m_words, 2) # "で"は2
        self.assertEqual(before_and_after, {'before': ['極東', 'アニメーション'] , 'after': ['素敵', 'な', '作品']})

    def test_nara_before_and_after(self):
        ad = self.chuni_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        before_and_after = ad.nara_before_and_after(m_words, 1) # "で"は2
        self.assertEqual(before_and_after, {'before': ['夢'] , 'after': ['たくさん', '見', 'た']})

    def test_nara_three_words(self):
        ad = self.chuni_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        before_and_after = ad.three_words_by_func(m_words, ad.nara_before_and_after)
        self.assertEqual(before_and_after, {'before': ['夢'] , 'after': ['たくさん', '見', 'た']})

    def test_nara_three_words_if_no_nara(self):
        ad = self.kyokuto_anime_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        before_and_after = ad.three_words_by_func(m_words, ad.nara_before_and_after)
        self.assertEqual(before_and_after, {'after': [], 'before': []})

    def test_nara_three_words_when_trigger_snippet_given(self):
        ad = self.trigger_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        result = ad.three_words_by_func(m_words, ad.nara_before_and_after)
        self.assertEqual(result,
            {
            'before': ['。', 'あの', '今石洋之'],
            'after': ['世界', 'を', '変え']
            }
        )

    def test_nara_three_words_of_nara_de_ha(self):
        ad = self.trigger_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        result = ad.three_words_of_nara_de_ha(m_words)
        self.assertEqual(result,
            {
                'なら': 
                    {
                    'before': ['。', 'あの', '今石洋之'],
                    'after': ['世界', 'を', '変え']
                    }
                ,
                'で': 
                    {
                    'before': ['TRIGGER', 'の', 'キルラキル'],
                    'after': ['アニメ', 'の', '新']
                    }
                ,
                'は':
                    {
                    'before': [],
                    'after': []
                    }
            }
        )

    def test_pick_characteristic_words(self):
        ad = self.trigger_snippet_ad
        ad.link_page_title = ad.title
        results = ad.pick_characteristic_words()
        expectation = {
            'なら': 
                {
                'before': ['。', 'あの', '今石洋之'],
                'after': ['世界', 'を', '変え']
                }
            ,
            'で': 
                {
                'before': ['TRIGGER', 'の', 'キルラキル'],
                'after': ['アニメ', 'の', '新']
                }
            ,
            'は':
                {
                'before': [],
                'after': []
                }
        }
        self.assertEqual(results[0], expectation)
        self.assertEqual(results[1], expectation)
        self.assertEqual(results[2], expectation)

if __name__ == '__main__':
    unittest.main()
