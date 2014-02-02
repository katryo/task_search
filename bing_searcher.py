from bing import Bing
import my_keys
from web_page import WebPage
import pdb


class BingSearcher():
    def __init__(self, query):
        self.query = query

    def _search(self, page_num):
        key = my_keys.MICROSOFT_API_KEY_2
        bing = Bing(key)
        items = bing.web_search(self.query, page_num, ['Title', 'Url', 'Description'])
        return items

    def result_pages(self, page_num=50):
        items = self._search(page_num)
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

