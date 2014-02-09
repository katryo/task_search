# -*- coding: utf-8 -*-
from object_term import ObjectTerm
import pdb


class Task(object):
    def __init__(self, object_term, cmp='を', predicate_term='', query='', order=0, url='',
                 is_shopping=False, is_official=False):
        self.object_term = object_term
        self.predicate_term = predicate_term
        self.query = query  # いらないのでは
        self.cmp = cmp
        self.order = order
        self.url = url
        self.is_shopping = is_shopping
        self.is_official = is_official


