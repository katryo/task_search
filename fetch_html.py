from search_engine import SearchEngine
import os
import pickle

QUERY = '家庭菜園　始める　方法'
DIR = 'gardening'


def search_and_fetch_30_pages():
    search_engine = SearchEngine()
    pages = search_engine.google_search(QUERY, 3)
    [page.fetch_html() for page in pages]
    return pages


if __name__ == '__main__':
    os.chdir('fetched_pages/gardening')
    pages = search_and_fetch_30_pages()
    for i, page in enumerate(pages):
        f = open(DIR + '_page_' + str(i) + '.pkl', 'wb')
        pickle.dump(page, f)
        f.close()