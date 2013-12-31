# -*- coding: utf-8 -*-
from sentence_separator import SentenceSeparator
import constants
import pdb
import re
STEP_WORDS = 'ステップ 手順 その'.split(' ')


class Labelable():
    '''
    HeadingやSentenceが継承する
    '''
    def __init__(self, text):
        self.body = self.remove_parenthesis(text)
        self.set_blank_if_not_includes_hiragana_or_karakana()
        self.body = self.remove_inside_round_parenthesis(self.body)
        sp = SentenceSeparator()
        self.m_body_words = sp.m_words(self.body)

    def set_blank_if_not_includes_hiragana_or_karakana(self):
        if not self.includes_hiragana_or_katakana():
            self.body = ''

    def includes_hiragana_or_katakana(self):
        katakana_pattern = re.compile('[ァ-ヾ]')
        hiragana_pattern = re.compile('[ぁ-ゞ]')
        if katakana_pattern.match(self.body) or hiragana_pattern.match(self.body):
            return True
        return False

    def remove_inside_round_parenthesis(self, text):
        for parentheses in constants.ROUND_PARENTHESIS:
            if parentheses in text:
                pattern_1 = re.compile('（.*?）')
                pattern_2 = re.compile('\(.*?\)')
                try:
                    text = pattern_1.sub(text, '')
                except:
                    pdb.set_trace()
                text = pattern_2.sub(text, '')
        return text



    def remove_parenthesis(self, text):
        for parentheses in constants.PARENTHESIS:
            text = text.replace(parentheses, '')
        return text


    def label_ends_with_verb(self):
        if self.m_body_words[-1].type == '動詞':
            self.features['ends_with_verb'] = True

    def label_starts_with_step_word(self):
        if self.is_starting_with_step_word():
            self.features['starts_with_step_word'] = True

    def is_starting_with_step_word(self):
        for w in STEP_WORDS:
            if self.body.startswith(w):
                return True
        return False

    def start_with_num(self):
        if self.body[0].isnumeric():
            return True
        return False

