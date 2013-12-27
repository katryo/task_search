__author__ = 'katouryou'
import os
import constants
import pickle
from web_page import WebPage
from pattern_matcher import PatternMatcher

def fetch_ads():
    query = constants.FINAL_QUERY
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


if __name__ == '__main__':
    if not os.path.exists(constants.FETCHED_ADS_DIR_NAME):
        os.mkdir(constants.FETCHED_AdS_DIR_NAME)
    os.chdir(constants.FETCHED_AdS_DIR_NAME)
    if not os.path.exists(constants.FINAL_QUERY):
        os.mkdir(constants.FINAL_QUERY)
    os.chdir(constants.FINAL_QUERY)
    for i, page in enumerate(pages):
        with open('%s_%i.pkl' % (constants.FINAL_QUERY, i), 'wb') as f:
            pickle.dump(page, f)


