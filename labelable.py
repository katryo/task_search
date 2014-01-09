# -*- coding: utf-8 -*-
import pdb
import re
from text_combiner import TextCombiner
from m_words_factory import MWordsFactory


class Labelable(object):
    '''
    HeadingやSentenceが継承する
    '''
    def __init__(self, text):
        tc = TextCombiner()
        self.body = tc.remove_parenthesis(text)
        self.set_blank_to_body_if_not_includes_hiragana_or_karakana()
        self.body = tc.remove_inside_round_parenthesis(self.body)
        m_factory = MWordsFactory()
        self.m_body_words = m_factory.build_from(self.body)

    def set_blank_to_body_if_not_includes_hiragana_or_karakana(self):
        if not self.includes_hiragana_or_katakana():
            self.body = ''

    def includes_hiragana_or_katakana(self):
        katakana_pattern = re.compile('[ァ-ヾ]')
        hiragana_pattern = re.compile('[ぁ-ゞ]')
        if katakana_pattern.search(self.body) or hiragana_pattern.search(self.body):
            return True
        return False


    def start_with_num(self):
        if self.body[0].isnumeric():
            return True
        return False

    def set_m_body_words_by_combine_words(self):
        tc = TextCombiner()
        self.m_body_words = tc.combine_nouns(self.m_body_words)
        self.m_body_words = tc.combine_verbs(self.m_body_words)

