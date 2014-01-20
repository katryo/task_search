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
        try:
            page_num_per_query = math.floor(total_page_num / (len(self.expansion_words) + 1))
        except ZeroDivisionError:
            pdb.set_trace()

        pages = []
        for query in self.queries():
            bs = BingSearcher(query)
            pages.extend(bs.result_pages(page_num_per_query))
        return pages

    def queries(self):
        queries = self.expansion_words
        queries.append(self.body)
        return queries