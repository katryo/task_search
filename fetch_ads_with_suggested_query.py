import os
import constants
import pickle
from web_page import WebPage
from path_mover import PathMover


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
    mover = PathMover()
    mover.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
    for query in constants.QUERIES:
        mover.go_or_create_and_go_to(query)

        mover.go_up()

    if not os.path.exists(constants.FINAL_QUERY):
        os.mkdir(constants.FINAL_QUERY)
    os.chdir(constants.FINAL_QUERY)
    for i, page in enumerate(pages):
        with open('%s_%i.pkl' % (constants.FINAL_QUERY, i), 'wb') as f:
            pickle.dump(page, f)


