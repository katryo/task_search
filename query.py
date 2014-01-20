# -*- coding: utf-8 -*-
import constants
from bing_searcher import BingSearcher
import math
import pdb


class Query:
    def __init__(self, body):
        self.body = body

    def set_expansion_words(self, words):
        self.expansion_words = words

    def search_with_expansion_words(self):
        total_page_num = constants.NUM_OF_TOTAL_FETCHED_PAGES
        page_num_per_query = math.floor(total_page_num / len(self.queries()))

        pages = dict()
        for query in self.queries():
            bs = BingSearcher(query)
            result_pages = bs.result_pages(page_num_per_query)
            pages[query] = result_pages
        return pages  # {'犬　育てる': [Page, Page,...], '犬　育てる　教育': [Page,...]}

    def queries(self):
        queries = []
        for word in self.expansion_words:
            queries.append(self.body + '　' + word)
        queries.append(self.body)
        return queries