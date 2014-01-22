# -*- coding: utf-8 -*-
from object_term import ObjectTerm
import pdb


class Task(object):
    def __init__(self, object_term='', cmp='', predicate_term='', context='', order=0, url=''):
        try:
            self.object_term = ObjectTerm(text=object_term, context=context)
        except TypeError:
            pdb.set_trace()
        self.cmp = cmp
        self.predicate_term = predicate_term
        self.context = context  # いらないのでは
        self.order = order
        self.url = url


