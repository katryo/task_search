# -*- coding: utf-8 -*-
import pdb
from pattern_matcher import PatternMatcher


class ToiuSearcher():
    def embody_search(self, term, context):
        query = '"という%s" %s' % (term, context)
        pm = PatternMatcher(query)
        pages = pm.bing_search()
        return pages
