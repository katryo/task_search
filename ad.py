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

    def three_words_before_and_after(self, mecabed_words):
        for i, m_word in enumerate(mecabed_words):
            for characteristic_word in ['なら', 'で', 'は']:
                if m_word.name == characteristic_word:
                    three_words_before = self.till_three_words_before(mecabed_words, i)
                    three_words_after = self.till_three_words_after(mecabed_words, i)
        return three_words_before + three_words_after

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
