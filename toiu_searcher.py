# -*- coding: utf-8 -*-
import pdb
from bing_searcher import BingSearcher


class ToiuSearcher():
    def result_pages(self, term, context):
        query = '"という%s" %s' % (term, context)
        bs = BingSearcher(query)
        pages = bs.result_pages()
        return pages


if __name__ == '__main__':
    ts = ToiuSearcher(term='ガンダム', context='趣味')
