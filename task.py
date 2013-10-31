from web_item import WebItem
from pyquery import PyQuery as pq

class Task(WebItem):
    def set_title_with_html(self, html):
        self.title = pq(html.encode('utf-8')).find('title').text()

    def set_url(self, url):
        self.url = url

    def set_steps(self, steps):
        self.steps = steps