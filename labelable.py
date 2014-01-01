# -*- coding: utf-8 -*-
from sentence_separator import SentenceSeparator
import constants
import pdb
import re
from text_combiner import TextCombiner
from mecabed_noun import MecabedNoun
from mecabed_verb import MecabedVerb
# STEP_WORDS = 'ステップ 手順 その'.split(' ')


class Labelable(TextCombiner):
    '''
    HeadingやSentenceが継承する
    '''
    def __init__(self, text):
        self.body = self.remove_parenthesis(text)
        self.set_blank_to_body_if_not_includes_hiragana_or_karakana()
        self.body = self.remove_inside_round_parenthesis(self.body)
        sp = SentenceSeparator()
        self.m_body_words = sp.m_words(self.body)

    def set_blank_to_body_if_not_includes_hiragana_or_karakana(self):
        if not self.includes_hiragana_or_katakana():
            self.body = ''

    def includes_hiragana_or_katakana(self):
        katakana_pattern = re.compile('[ァ-ヾ]')
        hiragana_pattern = re.compile('[ぁ-ゞ]')
        if katakana_pattern.search(self.body) or hiragana_pattern.search(self.body):
            return True
        return False



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

    def set_m_body_words_by_combine_words(self):
        self.m_body_words = self.combine_nouns(self.m_body_words)
        self.m_body_words = self.combine_verbs(self.m_body_words)

