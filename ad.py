# -*- coding: utf-8 -*-
import requests
import constants
import re
import pdb
from web_item import WebItem
from pyquery import PyQuery as pq


class Ad(WebItem):
    def __init__(self, title='', snippet='', link=''):
        self.title = title
        self.snippet = snippet
        self.link = link
        #linkは広告のWebページURLではなくyahooのURLを経由

    def fetch_link_title(self):
        self.fetch_html()
        self.set_page_title()

    def set_page_title(self):
        # Widows-31Jはムリ
        self.link_page_title = pq(self.html_body.encode(self.response.encoding)).find('title').text()

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
        items = [self.title, self.snippet]
        if self.link_page_title:
            items.append(self.link_page_title)
        for item in items:
            m_words = self.to_m_words(item)
            results.append(self.three_words_of_nara_de_ha(m_words))
            # results => [{'なら': {'before': ['。', 'あの', '今石洋之']}, 'で'}]
        return results

    def pick_bracket_words(self):
        results = []
        items = [self.title, self.snippet]
        if self.link_page_title:
            items.append(self.link_page_title)
        for text in items:
            results.extend(self.pick_bracket_words_from_text(text))
        return results

    def pick_bracket_words_from_text(self, text):
        brackets = list()
        brackets.append({'head': '「', 'tail': '」'})
        brackets.append({'head': '『', 'tail': '』'})
        brackets.append({'head': '"', 'tail': '"'})
        brackets.append({'head': '“', 'tail': '”'})
        brackets.append({'head': '《', 'tail': '》'})
        brackets.append({'head': '<<', 'tail': '>>'})
        brackets.append({'head': '【', 'tail': '】'})

        results = []
        for bracket in brackets:
            results_per_bracket_type = self.bracket_words_per_bracket_type(text, bracket['head'], bracket['tail'])
            # results_per_bracket_typeは[]になる場合が多い。
            if results_per_bracket_type: results.extend(results_per_bracket_type)
        return results

    def bracket_words_per_bracket_type(self, text, bracket_head, bracket_tail):
        #bracket_head, bracket_tail = '「', '」'
        # 広告に「」と『』、複数使っているものも取ってくる
        results = []
        # results => ["グルコサミン", "カビゴン"]
        if bracket_head in text:
            pattern = re.compile('%s.*?%s' % (bracket_head, bracket_tail))
            words_with_bracket = pattern.findall(text)
            stripped_words = self.strip_bracket(words_with_bracket, bracket_head, bracket_tail)
            results.extend(stripped_words)
        return results

    def strip_bracket(self, words_with_bracket, bracket_head, bracket_tail):
        stripped_words = []
        for word in words_with_bracket:
            stripped_word = word.strip(bracket_head).strip(bracket_tail)
            stripped_words.append(stripped_word)
        return stripped_words



    def three_words_of_nara_de_ha(self, m_words):
        # 話題', 'の', 'ドリップクリスナンリキッドタイプ
        # 'コーヒー豆', 'の', '通販'
        results = {}
        # なら => m_word.type == 助動詞
        # で => m_word.type == 助詞
        # は => type == 助詞 subtype == 係助詞
        # results['なら']['before'] => ['極東', 'アニメーション']
        results['nara'] = self.three_words_by_func(m_words, self.nara_before_and_after)
        results['de'] = self.three_words_by_func(m_words, self.de_before_and_after)
        results['ha'] = self.three_words_by_func(m_words, self.ha_before_and_after)
        # ""や「」や≪≫で囲んだものを入れては。
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
        result['before'] = self.up_to_three_words_before(m_words, i)
        result['after'] = self.up_to_three_words_after(m_words, i)
        return result

    def up_to_three_words_before(self, m_words, i):
        #TODO: Refactor later
        words = []

        first_m_word = self.is_over_or_m_word(m_words, i, 0, '名詞')
        if first_m_word == False:
            return []

        else:
            words.insert(0, first_m_word.name)

            if i == 1:
                # ['アニメ', 'なら']のようなとき。やはりめったにない
                return words
            second_m_word = m_words[i - 2]
            if second_m_word.type != '名詞' and second_m_word.name != 'の':
                # ['すごく', '動く', 'アニメ', 'なら']
                return words

            else:
                words.insert(0, second_m_word.name)

                third_m_word = self.is_over_or_m_word(m_words, i, 2, '名詞')
                if third_m_word == False:
                    return words

                #['ハイパー']
                words.insert(0, third_m_word.name)

                # どちらにせよwords返す
                # ['あの', 'グレート', 'アニメ', 'なら']
                return words

    def up_to_three_words_after(self, m_words, i):
        #TODO: Refactor later
        words = []
        size = len(m_words)
        
        first_m_word = self.is_after_over_or_m_word(m_words, i, 0, '名詞')
        if first_m_word == False:
            return []

        else:
            words.append(first_m_word.name)

            if i + 3 > size:
                # ['アニメ', 'なら']のようなとき。やはりめったにない
                return words
            second_m_word = m_words[i + 2]
            if second_m_word.type != '名詞' and second_m_word.name != 'の':
                # ['すごく', '動く', 'アニメ', 'なら']
                return words

            else:
                words.append(second_m_word.name)

                third_m_word = self.is_after_over_or_m_word(m_words, i, 2, '名詞')
                if third_m_word == False:
                    return words

                #['ハイパー']
                words.append(third_m_word.name)

                # どちらにせよwords返す
                # ['あの', 'グレート', 'アニメ', 'なら']
                return words


    def is_after_over_or_m_word(self, m_words, i, count, type):
        # count => 0, 1, 2
        if i + count + 2 > len(m_words):
            # after_over!
            return False
        m_word = m_words[i + count + 1]

        if not m_word.type == type:
        # ['で', '働く', 'なら']のような場合
            return False
        return m_word


    def is_over_or_m_word(self, m_words, i, count, type):
        # count => 0, 1, 2
        if i == count:
            # ['なら']だけのとき。めったにないと思う。
            return False
        first_m_word = m_words[i - count - 1]

        if not first_m_word.type == type:
        # ['で', '働く', 'なら']のような場合
            return False
        return first_m_word


    def till_three_words_before(self, mecabed_words, keyword_index):
        words_before_keyword_index = []
        for x in reversed(range(1, 4)):
            # keyword_index == 1
            # x == 3, 2, 1
            if x > keyword_index:
                continue
            # ここで、名詞、名詞と続いた場合にのみ答えに入れるようにしては
            # あるいは名詞、助詞、名詞のときのみ
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
