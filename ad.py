# -*- coding: utf-8 -*-
import requests
import pdb
from web_item import WebItem
from pyquery import PyQuery as pq
from word_picker import WordPicker


class Ad(WebItem):
    def __init__(self, title='', snippet='', link=''):
        self.title = title
        self.snippet = snippet
        self.link = link
        #linkは広告のWebページURLではなくyahooのURLを経由

    def fetch_link_title(self):
        self.fetch_html()
        self.set_page_title()

    def set_page_title(self):
        # Widows-31Jはムリ
        self.link_page_title = pq(self.html_body.encode(self.response.encoding)).find('title').text()

    def fetch_html(self):
        # WebItemのメソッドをオーバーライド
        response = requests.get(self.link)
        self.fetch_html_with_response(response)

    def sahens_in_snippet(self):
        wp = WordPicker(self.snippet)
        sahens = wp.pick_sahens()
        return sahens

    def sahens_in_title(self):
        wp = WordPicker(self.title)
        sahens = wp.pick_sahens()
        return sahens

    def sahens_from_title_and_snippet(self):
        sahens = self.sahens_in_snippet()
        sahens.extend(self.sahens_in_title())
        return sahens

    def set_sahens_from_title_and_snippet(self):
        sahens = self.sahens_from_title_and_snippet()
        self.sahens = sahens