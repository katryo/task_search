# -*- coding: utf-8 -*-
import pdb
import utils

class ToiuSearcher():
    def embody_search(self, term, context):
        query = '"という%s" %s' % (term, context)
        pages = utils.search_web_pages(query)
        return pages


if __name__ == '__main__':
    ts = ToiuSearcher(term='ガンダム', context='趣味')
