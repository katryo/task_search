from search_engine import SearchEngine
from bing import Bing
import my_keys
from web_page import WebPage
import pdb


class PatternMatcher():
    def __init__(self, query):
        self.query = query
        self.search_num = 1

    def google_search(self):
        engine = SearchEngine()
        pages = engine.google_search(self.query, self.search_num)
        return pages

    def bing_search(self):
        key = my_keys.MICROSOFT_API_KEY
        bing = Bing(key)
        items = bing.web_search(self.query, 50, ['Title', 'Url', 'Description'])
        pages = []
        for item in items:
            if type(item) == str:
                continue
            page = WebPage(item['Url'])
            page.query = self.query
            #googleの書き方に統一
            page.title = item['Title']
            page.snippet = item['Description']
            pages.append(page)
        return pages

