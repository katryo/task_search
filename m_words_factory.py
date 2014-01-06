# -*- coding: utf-8 -*-
__author__ = 'katouryou'
import MeCab
from mecabed_word import MecabedWord


class MWordsFactory(object):
    def build_from(self, text):
        tagger = MeCab.Tagger('mecabrc')
        result = tagger.parse(text)
        word_info_collection = result.split('\n')
        m_words = []
        for info in word_info_collection:
            #infoが',\t名詞,サ変接続,*,*,*,*,*'のようなときはbreakする
            if info == 'EOS' or info == '':
                break
            else:
                invalid = self.includes_invalid_word(info)
                if invalid is True:
                    break
                else:
                    mw = MecabedWord(info)
                    #mw.name => '希望'
                    #mw.type => '名詞'
                    #mw.subtype => 'サ変接続'
                    m_words.append(mw)
        return m_words

    def includes_invalid_word(self, info):
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
