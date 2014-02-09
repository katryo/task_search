# -*- coding: utf-8 -*-
import pdb
from task_data_inserter import TaskDataInserter


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

        tdi = TaskDataInserter()
        if not tdi.has(query=self.query,
                       url=self.url,
                       noun=object_term,
                       cmp=cmp,
                       verb=predicate_term):
            tdi.insert(query=self.query,
                       url=self.url,
                       noun=object_term,
                       cmp=cmp,
                       verb=predicate_term)
