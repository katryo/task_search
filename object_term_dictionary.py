# -*- coding: utf-8 -*-
import pdb

class ObjectTermDictionary(object):
    """
    otdは、シングルトン。「こういうobject_termはないですか？」とTaskが問い合わせに来る。
    otを追加したり。
    """
    def __init__(self):
        self.object_terms = []

    def contains(self, term):
        if term in self.object_terms:
            return True
        return False

    def add(self, term):
        if self.contains(term):
            return
        self.object_terms.append(term)

    def embodied_terms(self, term='', context=''):
        for object_term in self.object_terms:
            if str(object_term) == term and object_term.context == context:
                return object_term.embodied_terms
        return []

"""
    def embodied_term_by_search(self, term):
        という検索で、「具体化した語」を求める
        query = '"という%s" %s' % (term.name, term.context)
        pm = PatternMatcher(query)
        pages = pm.bing_search()
        terms = []
        for page in pages:
            m_words = self.prepare_m_words(page)
            try:
                for i, m_word in enumerate(m_words):
                    if m_word.name == term.name:  # 薬
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

"""