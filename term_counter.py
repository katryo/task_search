# -*- coding: utf-8 -*-
import pdb
import constants

class TermCounter(object):
    def __init__(self):
        self.term_count = {}
        
    # set_sahens_from...のあと、これでself.sahen_countができあがる
    def count_terms(self, terms=['a']):
        for term in terms:
            self._count_up(term)

    def _count_up(self, word):
        if word in self.term_count:
            self.term_count[word] += 1
            return
        self.term_count[word] = 1

    def frequent_terms(self):
        threshold = 1
        results = []
        for word in self.term_count:
            if word in constants.STOPWORDS:
                continue
            if self.term_count[word] > threshold:
                results.append(word)
        return results