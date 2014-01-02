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
        for object_term in self.object_terms:
            if term.name == object_term.name:
                if term.context == object_term.context:
                    return True
        return False

    def add(self, term):
        if self.contains(term):
            return False
        self.object_terms.append(term)

    def embodied_terms(self, term='', context=''):
        for object_term in self.object_terms:
            if str(object_term) == term and object_term.context == context:
                return object_term.embodied_terms
        return []

