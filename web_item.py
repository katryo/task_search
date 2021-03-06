# -*- coding: utf-8 -*-
from mecabed_word import MecabedWord
import requests
import pdb
import cchardet
import MeCab
import re
import sys
from sentence_separator import SentenceSeparator
from mecabed_noun import MecabedNoun
from task import Task
from object_term_dictionary import ObjectTermDictionary

class WebItem():

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            self.fetch_html_with_response(response)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.TooManyRedirects):
            self.html_body = ''

    def fetch_html_with_response(self, response):
        encoding_detected_by_cchardet = cchardet.detect(response.content)['encoding']
        response.encoding = encoding_detected_by_cchardet
        html_body = response.text
        self.response = response  # Adのために作った

        script_pattern = re.compile('<script.*?<\/script>')
        self.html_body = script_pattern.sub('', html_body)

    def past_text(self, i, m_word, m_words):
        """
- もし「た」の直前が「サ変・スル」だったら、さらに前の語 + した
- 「た」の直前が「サ変・スル」で、その直前が「を」だったら、さらにさらに前の語 + をした
        """
        if m_word.word_info == 'た\t助動詞,*,*,*,特殊・タ,基本形,た,タ,タ':
            if 'サ変・スル' in m_words[i-1].word_info:
                if 'を' in m_words[i-2].word_info:
                    return m_words[i-3].stem  #運動をした
                return m_words[i-2].stem # 運動した

            # もし「なった」ならその前の「綺麗」から使う
            if 'なる,ナッ,ナッ' in m_words[i-1].word_info:
                return m_words[i-3].name + m_words[i-2].name + 'なった'

            # '噛まれた'
            if '動詞,接尾,*,*,一段,連用形,れる,レ,レ' in m_words[i-1].word_info:
                return m_words[i-2].stem

            if '助動詞,*,*,*,特殊・マス,連用形,ます,マシ,マシ' in m_words[i-1].word_info:
                if 'サ変・スル' in m_words[i-2].word_info:
                    if 'を' in m_words[i-3].word_info:
                        return m_words[i-4].stem #クリアをしました

                # あっぱれでございました
                if m_words[i-2].name == 'ござい':
                    return False

                # なりました
                if m_words[i-2].name == 'なり':
                    return m_words[i-4].stem + m_words[i-3].stem

                return m_words[i-2].stem  # 噛みました

            # 「た」があって、その直前が「サ変・スル」じゃなかったら、その前 + た
            return m_words[i-1].stem  # 動いた
        return False

    def set_past_word_count(self):
        # self.sentencesはすでにある前提
        if not hasattr(self, 'past_word_count'):
            self.past_word_count = {}
        for sentence_index, sentence in enumerate(self.sentences):
            m_words = SentenceSeparator.m_words(sentence)
            for i, m_word in enumerate(m_words):
                # iはm_wordに分けたあとの順番
                past_text = self.past_text(i, m_word, m_words)
                if past_text:
                    self.past_word_count_up(past_text)

    def past_word_count_up(self, text):
        if text in self.past_word_count:
            self.past_word_count[text] += 1
            return
        self.past_word_count[text] = 1


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



    def remove_html_tags(self):
        tag_pattern = re.compile('<.*?>')
        self.html_body = tag_pattern.sub('', self.html_body)

        tag_tail_pattern = re.compile('.*>')
        self.html_body = tag_tail_pattern.sub('', self.html_body)

        tag_head_pattern = re.compile('<.*')
        self.html_body = tag_head_pattern.sub('', self.html_body)

    def combine_nouns(self, m_words):
        """
        再帰的に合体させる
        :param m_words:
        :return:
        """
        new_m_words = self.try_combine_nouns(m_words)
        # 合致するまで=変化しなくなるまで繰り返す
        if new_m_words == m_words:
            return m_words
        else:
            return self.combine_nouns(new_m_words)

    def try_combine_nouns(self, m_words):
        for i, m_word in enumerate(m_words):
            # 最後の単語は次がないので連続しない
            # m_words == [m_word]のとき i == 0, len(m_words) == 1
            if i + 1 == len(m_words):
                break
                # 名詞を見つけたら、その次の単語が名詞か調べる
            if m_word.type == '名詞':
                if m_words[i + 1].type == '名詞':
                    # やった！ 見つけたぞ！
                    # 名詞、名詞のコンボがあれば、m_wordsを再構成する
                    new_m_words = self.combine_to_one_noun(m_words, i)
                    return new_m_words
        return m_words

    def combine_to_one_noun(self, m_words, i):
        left_m = m_words[i]
        right_m = m_words[i + 1]
        combined_m = MecabedNoun(left_m.name + right_m.name)
        if i == 0 and len(m_words) == i + 2:
            return [combined_m]
        if i == 0 and len(m_words) != i + 2:
            m_words_after_combine = [combined_m] + m_words[i + 2:]
            return m_words_after_combine
        if i != 0 and len(m_words) == i + 2:
            m_words_after_combine = m_words[:i] + [combined_m]
            return m_words_after_combine
        m_words_after_combine = m_words[:i] + [combined_m] + m_words[i + 2:]
        return m_words_after_combine

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

    def set_text_from_html_body(self):
        html_tag_pattern = re.compile('<.*?>')
        tab_pattern = re.compile('\t')
        break_pattern = re.compile('\n')
        break_pattern_r = re.compile('\r')
        semicolon_pattern = re.compile(';\n')
        script_tag_pattern = re.compile('<script.*?</script>')
        brace_pattern = re.compile('\{.*?\}')
        text = semicolon_pattern.sub('', self.html_body)
        text = script_tag_pattern.sub('', text)
        text = tab_pattern.sub('', text)
        text = break_pattern.sub('', text)
        text = break_pattern_r.sub('', text)
        text = brace_pattern.sub('', text)
        text = text.replace(' ', '').replace('　', '')
        self.text = html_tag_pattern.sub('', text)

    def set_verbs_from_text(self):
        self.verbs = SentenceSeparator.verbs(self.text)

    def set_sahens_from_text(self):
        self.sahens = SentenceSeparator.sahens(self.text)

    def noun_before_query(self, sentence, query):
        # ValueErrorが出るかも
        i = sentence.index(query)
        # IndexErrorが出るかも
        suspicious_sentence = sentence[i-20:i]
        m_words = self.to_m_words(suspicious_sentence)
        m_words = self.combine_nouns(m_words)
        if m_words[-1].type == '名詞':
            return m_words[-1].name

