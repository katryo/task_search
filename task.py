# -*- coding: utf-8 -*-
import pdb
from task_data_inserter import TaskDataInserter
from task_data_selector import TaskDataSelector
from object_term import ObjectTerm
import constants


class Task(object):
    def __init__(self, distance_between_subtypes, object_term, cmp='を', predicate_term='',
                  query='', order=0, url='',
                 is_shopping=False, is_official=False,
                 rank=1000, sentence=''):
        object_term_obj = ObjectTerm(text=object_term, query=query)
        self.object_term = object_term_obj
        self.predicate_term = predicate_term
        self.distance_between_subtypes = distance_between_subtypes  # {'シャワールーム': -3, ...}
        self.query = query
        self.cmp = cmp
        self.order = order
        self.url = url
        self.is_shopping = is_shopping
        self.is_official = is_official
        self.rank = rank
        self.sentence = sentence

    def task_name(self):
        return '%s_%s_%s' % (self.object_term.name,
                             self.cmp,
                             self.predicate_term)

    def is_noise(self):
        threshold = constants.THRESHOLD_FOR_FREQUENTLY_APPERING_TASK
        selector = TaskDataSelector()
        num_of_queries = selector.num_of_queries()
        num_of_queries_contain_self = selector.num_of_queries_contain_ncv(
            noun=self.object_term.core_noun,
            cmp=self.cmp,
            verb=self.predicate_term
        )

        ratio = num_of_queries_contain_self / num_of_queries
        print('クエリごとの、このタスク「%s%s%s」の出現比率は%f' % (
            self.object_term.core_noun,
            self.cmp,
            self.predicate_term,
            ratio)
        )
        if ratio > threshold:
            print('%s_%s_%sはノイズです' % (
                self.object_term.core_noun,
                self.cmp,
                self.predicate_term)
            )
            return True
        return False
