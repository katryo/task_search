import requests
import constants
import pdb
from web_item import WebItem
from pyquery import PyQuery as pq


class Ad(WebItem):
    def __init__(self, args={'title': '', 'snippet': '', 'link': ''}):
        self.title = args['title']
        self.snippet = args['snippet']
        self.link = args['link']
        #linkは広告のWebページURLではなくyahooのURLを経由

    def fetch_link_title(self):
        self.fetch_html()
        self.set_page_title()

    def set_page_title(self):
        # Widows-31Jはムリ
        if self.encoding == 'Windows-31J':
            self.link_page_title = self.encoding
            return
        self.link_page_title = pq(self.html_body.encode(self.encoding)).find('title').text()

    def fetch_html(self):
        # WebItemのメソッドをオーバーライド
        response = requests.get(self.link)
        self.fetch_html_with_response(response)

    def fetch_ad_pages(self):
        words = constants.TASK_WORDS
        self.texts = self.find_words(words, self.link)
        #texts => ['水がおすすめ', '気をつけてください']


    def pick_characteristic_words(self):
        if not self.link_page_title: self.fetch_link_title()
        results = []
        for item in [self.title, self.snippet, self.link_page_title]:
            m_words = self.to_m_words(item)
            results.append(self.three_words_of_nara_de_ha(m_words))
            # results => [{'なら': {'before': ['。', 'あの', '今石洋之']}, 'で'}]
        return results

    def three_words_of_nara_de_ha(self, m_words):
        results = {}
        # なら => m_word.type == 助動詞
        # で => m_word.type == 助詞
        # は => type == 助詞 subtype == 係助詞
        # results['なら']['before'] => ['極東', 'アニメーション']
        results['なら'] = self.three_words_by_func(m_words, self.nara_before_and_after)
        results['で'] = self.three_words_by_func(m_words, self.de_before_and_after)
        results['は'] = self.three_words_by_func(m_words, self.ha_before_and_after)
        # results => {'なら': {'before': ['極東', 'アニメーション'], 'after': ['素敵', 'な', '作品']}, 'で': None, 'は': None}
        return results

    def three_words_by_func(self, m_words, func):
        # example: ad.three_words_by_func(m_words, ad.nara_before_and_after)
        # funcにはself.ha_before_and_afterなどが入る
        result = {}
        for i, m_word in enumerate(m_words):
            result_words = func(m_words, i)
            if result_words:
                result = result_words
                # 1つでも見つけたらそれで終わり。「…なら…なら……」広告は希少
                break
        # {'before': ['極東', 'アニメーション'], 'after': ['素敵', 'な', '作品']}
        if result == {}:
            result = {'before': [], 'after': []}
        return result


    def ha_before_and_after(self, m_words, i):
        # もっと複雑なm_wordsパターンマッチングも可能
        if m_words[i].name == "は" and m_words[i].type == "助詞" and m_words[i].subtype == "係助詞":
            return self.get_3_words_before_and_after(m_words, i)
        # return {'before': ['極東', 'アニメーション'], 'after': ['素敵', 'な', '作品']}
        return None

    def de_before_and_after(self, m_words, i):
        if m_words[i].name == "で" and m_words[i].type == "助詞":
            return self.get_3_words_before_and_after(m_words, i)
        # return {'before': ['極東', 'アニメーション'], 'after': ['素敵', 'な', '作品']}
        return None

    def nara_before_and_after(self, m_words, i):
        if m_words[i].name == "なら" and m_words[i].type == "助動詞":
            return self.get_3_words_before_and_after(m_words, i)
        # return {'before': ['極東', 'アニメーション'], 'after': ['素敵', 'な', '作品']}
        return None

    def get_3_words_before_and_after(self, m_words, i):
        result = {'before': [], 'after': []}
        # result => {'before': ['極東', 'アニメーション'], 'after': ['素敵', 'な', '作品']}
        result['before'] = self.till_three_words_before(m_words, i)
        result['after'] = self.till_three_words_after(m_words, i)
        return result


    def till_three_words_before(self, mecabed_words, keyword_index):
        words_before_keyword_index = []
        for x in reversed(range(1, 4)):
            # keyword_index == 1
            # x == 3, 2, 1
            if x > keyword_index:
                continue
            words_before_keyword_index.append(mecabed_words[keyword_index - x].name)
        return words_before_keyword_index

    def till_three_words_after(self, mecabed_words, keyword_index):
        words_after_keyword_index = []
        for x in range(1, 4):
            # keyword_index == 1
            # x == 3, 2, 1
            if x + keyword_index > len(mecabed_words) - 1:
                break
            words_after_keyword_index.append(mecabed_words[keyword_index + x].name)
        return words_after_keyword_index
