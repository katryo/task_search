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
        self.fetch_link_title()
        for item in [self.title, self.snippet, self.link_page_title]:
            m_words = self.to_m_words(item)
            self.nara_phrase(m_words)
   # good_phrases => ["ドッグフードなら楽天へ", "マンガならマンガ館", ...]

    def three_words_before_and_after(self, m_words):
        results = {}
        for i, m_word in enumerate(m_words):
            for characteristic_word in ['なら', 'で', 'は']:
                # results['なら']['before'] => ['極東', 'アニメーション']
                results[characteristic_word] = self.before_and_after_words_per_characteristic_word(m_words, characteristic_word, i)
        # results => {'なら': {'before': [], 'after': []}, 'で': {'before': [], 'after': []}, 'は': {'before': [], 'after': []}}
        return results

    def before_and_after_words_per_characteristic_word(self, m_words, characteristic_word, i):
        before_and_after = {'before': [], 'after': []}
        if m_words[i].name == characteristic_word:
            before_and_after['before'] = self.till_three_words_before(m_words, i)
            before_and_after['after'] = self.till_three_words_after(m_words, i)
        # before_and_after => {'before': ['極東', 'アニメーション'], 'after': ['素敵', 'な', '作品']}
        return before_and_after


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
