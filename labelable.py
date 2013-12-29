# -*- coding: utf-8 -*-
from web_item import WebItem
from sentence_separator import SentenceSeparator

STEP_WORDS = 'ステップ 手順 その'.split(' ')


class Labelable(WebItem):
    '''
    HeadingやSentenceが継承する
    '''
    def __init__(self, text):
        self.body = text
        sp = SentenceSeparator()
        self.m_body_words = sp.m_words(self.body)

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

    def label_starts_with_num(self):
        if self.is_starting_with_num():
            self.features['starts_with_num'] = True
            # 初期値がFalseなのでFalseのときset不要

    def is_starting_with_num(self):
        if self.body[0].isnumeric():
            return True
        return False

