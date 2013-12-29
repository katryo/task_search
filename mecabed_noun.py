# -*- coding: utf-8 -*-
from mecabed_word import MecabedWord


class MecabedNoun(MecabedWord):
    def __init__(self, word):
        super().__init__(word)
        self.name = word
        self.type = '名詞'
        self.subtype = '合成'