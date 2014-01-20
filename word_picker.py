# -*- coding: utf-8 -*-
from m_words_factory import MWordsFactory


class WordPicker(object):
    def __init__(self, body):
        self.body = body

    def pick_nouns_and_verbs(self):
        types = ['名詞', '動詞']
        keywords = self.pick_words_by_types(types)
        return keywords

    def pick_words_by_types(self, types):
        keywords = []
        mw_factory = MWordsFactory()
        m_words = mw_factory.build_from(self.body)
        for m_word in m_words:
            for word_type in types:
                if m_word.type == word_type:
                    keywords.append(m_word.name)
        return keywords

    def pick_words_by_type(self, typ):
        types = [typ]
        keywords = self.pick_words_by_types(types)
        return keywords

    def pick_sahens(self):
        keywords = []
        mw_factory = MWordsFactory()
        m_words = mw_factory.build_from(self.body)
        for m_word in m_words:
            if m_word.subtype == 'サ変接続':
                item = m_word.name
                keywords.append(item)
        return keywords

    def pick_verbs(self):
        keywords = self.pick_words_by_type('動詞')
        return keywords
