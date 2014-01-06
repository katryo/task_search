from bing import Bing
import my_keys
from web_page import WebPage
import pdb


class BingSearcher():
    def __init__(self, query):
        self.query = query
        self.search_num = 1

    def search(self):
        key = my_keys.MICROSOFT_API_KEY
        bing = Bing(key)
        items = bing.web_search(self.query, 50, ['Title', 'Url', 'Description'])
        return items

    def result_pages(self):
        items = self.search()
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

