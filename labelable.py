# -*- coding: utf-8 -*-
from sentence_separator import SentenceSeparator
import constants
import re
STEP_WORDS = 'ステップ 手順 その'.split(' ')


class Labelable():
    '''
    HeadingやSentenceが継承する
    '''
    def __init__(self, text):
        text = self.remove_parenthesis(text)
        self.body = self.remove_inside_round_parenthesis(text)
        sp = SentenceSeparator()
        self.m_body_words = sp.m_words(self.body)

    def remove_inside_round_parenthesis(self, text):
        for parentheses in constants.ROUND_PARENTHESIS:
            if parentheses in text:
                pattern_1 = re.compile('（.*?）')
                pattern_2 = re.compile('\(.*?\)')
                text = pattern_1.sub(text, '')
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

