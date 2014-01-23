# -*- coding: utf-8 -*-
from object_term import ObjectTerm
import pdb


class Task(object):
    def __init__(self, object_term, predicate_term='', query='', order=0, url=''):
        self.object_term = object_term
        self.predicate_term = predicate_term
        self.query = query  # いらないのでは
        self.order = order
        self.url = url


