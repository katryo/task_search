# -*- coding: utf-8 -*-
from web_page import WebPage


class AdFetcher(object):
    def fetch_ads(self, query='犬　育てる'):
        head = 'http://search.yahoo.co.jp/search/ss?p='
        tail = '&ei=UTF-8&fr=top_ga1_sa&type=websearch&x=drt'
        url = head + query + tail
        y_ad_page = WebPage(url)
        y_ad_page.fetch_html()
        y_ad_page.set_ads_with_html_body()
        sahens = []
        for ad in y_ad_page.ads:
            sahens.extend(ad.pick_sahens(ad.title))
            sahens.extend(ad.pick_sahens(ad.snippet))
