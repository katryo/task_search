import unittest
from ad import Ad
import pdb

class TestAd(unittest.TestCase):

    def setUp(self):
        self.kyokuto_anime_snippet_ad = Ad({'title': 'a', 'snippet': '極東アニメーションで素敵な作品を描こう', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        self.chuni_snippet_ad = Ad({'title': 'a', 'snippet': '夢ならたくさん見た', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        self.health_title_ad = Ad({'title': '健康を気にするなら', 'snippet': 's', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        self.trigger_snippet_ad = Ad({'title': 'TRIGGERのキルラキルでアニメの新世界を見よう。あの今石洋之なら世界を変えられる！', 'snippet': 'TRIGGERのキルラキルでアニメの新世界を見よう。あの今石洋之なら世界を変えられる！', 'link': 'http://www.pref.nara.jp/item/83513.htm'})
        self.sakuga_snippet_ad = Ad({'title': 't', 'snippet': 'あのグレートウルトラアニメなら銀河特急新幹線を超えられる', 'link': 'http://www.pref.nara.jp/item/83513.htm'})

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
        self.assertEqual(before_and_after, {'before': ['極東', 'アニメーション'] , 'after': ['素敵']})

    def test_nara_before_and_after(self):
        ad = self.chuni_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        before_and_after = ad.nara_before_and_after(m_words, 1) # "で"は2
        self.assertEqual(before_and_after, {'before': ['夢'] , 'after': ['たくさん']})

    def test_nara_three_words(self):
        ad = self.chuni_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        before_and_after = ad.three_words_by_func(m_words, ad.nara_before_and_after)
        self.assertEqual(before_and_after, {'before': ['夢'] , 'after': ['たくさん']})

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
            'before': ['今石洋之'],
            'after': ['世界']
            }
        )

    def test_nara_three_words_of_nara_de_ha(self):
        ad = self.trigger_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        result = ad.three_words_of_nara_de_ha(m_words)
        self.assertEqual(result,
            {
                'nara': 
                    {
                    'before': ['今石洋之'],
                    'after': ['世界']
                    }
                ,
                'de': 
                    {
                    'before': ['TRIGGER', 'の', 'キルラキル'],
                    'after': ['アニメ', 'の']
                    }
                ,
                'ha':
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
            'nara': 
                {
                'before': ['今石洋之'],
                'after': ['世界']
                }
            ,
            'de': 
                {
                'before': ['TRIGGER', 'の', 'キルラキル'],
                'after': ['アニメ', 'の']
                }
            ,
            'ha':
                {
                'before': [],
                'after': []
                }
        }
        self.assertEqual(results[0], expectation)
        self.assertEqual(results[1], expectation)
        self.assertEqual(results[2], expectation)

    def test_pick_bracket_words(self):
        ad = self.trigger_snippet_ad
        text = '《アスコルビン酸》で健康になろう'
        results = ad.pick_bracket_words_from_text(text)
        expectation = 'アスコルビン酸'
        self.assertEqual(results[0], expectation)

    def test_pick_double_bracket_words(self):
        ad = self.trigger_snippet_ad
        text = '<<すごい薬>>で健康になろう'
        results = ad.pick_bracket_words_from_text(text)
        expectation = 'すごい薬'
        self.assertEqual(results[0], expectation)

    def test_pick_single_bracket_words(self):
        ad = self.trigger_snippet_ad
        text = '<<すごい薬で健康になろう'
        results = ad.pick_bracket_words_from_text(text)
        expectation = []
        self.assertEqual(results, expectation)

    def test_up_to_three_words_before(self):
        ad = self.sakuga_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        words = ad.up_to_three_words_before(m_words, 4)
        expectation = ['グレート', 'ウルトラ', 'アニメ']
        self.assertEqual(words, expectation)

    def test_up_to_three_words_after(self):
        ad = self.sakuga_snippet_ad
        m_words = ad.to_m_words(ad.snippet)
        words = ad.up_to_three_words_after(m_words, 4)
        expectation = ['銀河', '特急', '新幹線']
        self.assertEqual(words, expectation)

if __name__ == '__main__':
    unittest.main()
