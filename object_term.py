# -*- coding: utf-8 -*-
import pdb
from sentence_separator import SentenceSeparator
from text_combiner import TextCombiner


class ObjectTerm():
    """
    目的語オブジェクト。たいていの場合は名詞。「という検索」により、具体化した語（instance-of関係）や
    抽象化した語（逆instance-of関係）を探せる。
    """
    def __init__(self, text='', context=''):
        self.name = text
        self.context = context  # contextはたいてい検索クエリが入る。

    def embodied_term_by_search(self, pages):
        """
        という検索で、「具体化した語」を求める
        """
        terms = []
        for page in pages:
            m_words = self.prepare_m_words(page)
            try:
                for i, m_word in enumerate(m_words):
                    if m_word.name == self.name:  # 薬
                        if m_words[i-1].name == 'という':  # という薬
                            m_word_before_toiu = m_words[i-2]  # ?という薬
                            if m_word_before_toiu.type == '名詞':  #<名詞>という薬
                                if m_word_before_toiu.is_mono_kotoba_etc():
                                    continue
                                terms.append(m_word_before_toiu.name)
            except IndexError:
                continue
        return terms

    def prepare_m_words(self, page):
        tc = TextCombiner()
        sp = SentenceSeparator()
        snippet = tc.remove_all_parenthesis(page.snippet)
        m_words = sp.m_words(snippet)
        m_words = tc.combine_nouns(m_words)
        m_words = tc.combine_verbs(m_words)
        return m_words

    def set_embodied_terms_to_term_by_search(self, term):
        terms = self.embodied_term_by_search()
        term.embodied_terms = terms

