# -*- coding: utf-8 -*-
from ad_page import AdPage


class AdFetcher(object):
    def __init__(self, query):
        self.query = query

    def fetch_ads(self):
        head = 'http://search.yahoo.co.jp/search/ss?p='
        tail = '&ei=UTF-8&fr=top_ga1_sa&type=websearch&x=drt'
        url = head + self.query + tail
        ad_page = AdPage(url)
        ad_page.fetch_html()
        ad_page.set_ads_with_html_body()
        return ad_page.ads


        #sahens = []
        #for ad in ad_page.ads:
        #    sahens.extend(ad.pick_sahens(ad.title))
        #    sahens.extend(ad.pick_sahens(ad.snippet))
