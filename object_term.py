# -*- coding: utf-8 -*-
from pattern_matcher import PatternMatcher
from sentence_separator import SentenceSeparator
from text_combiner import TextCombiner


class ObjectTerm(str):
    """
    目的語オブジェクト。たいていの場合は名詞。「という検索」により、具体化した語（instance-of関係）や
    抽象化した語（逆instance-of関係）を探せる。
    """
    def embodied_term_by_search(self, context):
        """
        という検索で、「具体化した語」を求める
        """
        query = '"という%s" %s' % (self.__str__, context)
        pm = PatternMatcher(query)
        pages = pm.bing_search()
        terms = []
        for page in pages:
            m_words = self.prepare_m_words(page)
            try:
                for i, m_word in enumerate(m_words):
                    if m_word.name == self.__str__:  # 薬
                        if m_words[i-1].name == 'という': # という薬
                            m_word_before_toiu = m_words[i-2] # ?という薬
                            if m_word_before_toiu.type == '名詞': #<名詞>という薬
                                if m_word_before_toiu.is_mono_kotoba_etc():
                                    continue
                                terms.append(m_word_before_toiu.name)
            except IndexError:
                continue
        return terms

    def prepare_m_words(self, page):
        tc = TextCombiner()
        sp = SentenceSeparator
        snippet = tc.remove_all_parenthesis(page.snippet)
        m_words = sp.m_words(snippet)
        m_words = tc.combine_nouns(m_words)
        m_words = tc.combine_verbs(m_words)
        return m_words

    def set_embodied_term_by_search(self, context):
        terms = self.embodied_term_by_search(context)
        self.embodied_terms = terms

