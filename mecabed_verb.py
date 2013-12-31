# -*- coding: utf-8 -*-
from mecabed_word import MecabedWord


class MecabedVerb(MecabedWord):
    def __init__(self, word):
        super().__init__(word)
        self.name = word
        self.type = '動詞'
        self.subtype = '合成'