from mecabed_word import MecabedWord
from pyquery import PyQuery as pq
import requests
import pdb
import cchardet
import MeCab
import re
import sys


class WebItem():

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            self.fetch_html_with_response(response)
        except ConnectionError:
            self.html_body = ''

    def fetch_html_with_response(self, response):
        encoding_detected_by_cchardet = cchardet.detect(response.content)['encoding']
        response.encoding = encoding_detected_by_cchardet
        html_body = response.text
        self.response = response  # Adのために作った

        script_pattern = re.compile('<script.*?<\/script>')
        self.html_body = script_pattern.sub('', html_body)

    def pick_words_by_types(self, string, types):
        keywords = []
        m_words = self.to_m_words(string)
        for m_word in m_words:
            for word_type in types:
                if m_word.type == word_type:
                    keywords.append(m_word.name)
        return keywords

    def pick_words_by_type(self, string, type):
        types = [type]
        keywords = self.pick_words_by_types(string, types)
        return keywords

    def pick_sahens(self, string):
        keywords = []
        m_words = self.to_m_words(string)
        for m_word in m_words:
            if m_word.subtype == 'サ変接続':
                item = m_word.name
                keywords.append(item)
        return keywords

    def pick_verbs(self, str):
        keywords = self.pick_words_by_type(str, '動詞')
        return keywords

    def to_m_words(self, str):
        tagger = MeCab.Tagger('mecabrc')
        result = tagger.parse(str)
        word_info_collection = result.split('\n')
        m_words = []
        for info in word_info_collection:
            #infoが',\t名詞,サ変接続,*,*,*,*,*'のようなときはbreakする
            if info == 'EOS' or info == '':
                break
            else:
                invalid = self.is_including_invalid_word(info)
                if invalid is True:
                    break
                else:
                    mw = MecabedWord(info)
                    #mw.name => '希望'
                    #mw.type => '名詞'
                    #mw.subtype => 'サ変接続'
                    m_words.append(mw)
        return m_words

    def is_including_invalid_word(self, info):
        head = info[0:4]
        invalid = False
        invalid_words = [
            ',', '.', '…', '(', ')', '-',
            '/', ':', ';', '&', '%', '％',
            '~', '〜', '≪', '≫', '[', ']',
            '|', '"'
        ]
        for invalid_word in invalid_words:
            if invalid_word in head:
                invalid = True
                break
        return invalid

    def pick_nouns_and_verbs(self, str):
        types = ['名詞', '動詞']
        keywords = self.pick_words_by_types(str, types)
        return keywords

    def remove_tags(self, noisy_sentence):
        '''
        '/>aaaa'や<bold>などタグの入ったnoisy_sentenceからタグを消す。
        タグの部分、 /> や < もあるかもしれないので消す。
        '''
        # まず完全なタグが入っている場合
        tag_pattern = re.compile('<.*?>')
        noisy_sentence = tag_pattern.sub('', noisy_sentence)

        tag_tail_pattern = re.compile('.*>')
        noisy_sentence = tag_tail_pattern.sub('', noisy_sentence)

        tag_head_pattern = re.compile('<.*')
        noisy_sentence = tag_head_pattern.sub('', noisy_sentence)

        return noisy_sentence
