from search_engine import SearchEngine
import pickle
import os

QUERY = '家庭菜園　始める　方法'
DIR = 'gardening'


class LocalController():
    def search_and_fetch_headers(self):
        pages = self.search_30_pages()
        results = []
        for page in pages:
            page.fetch_html()
            page.build_heading_tree()

            # result[0] => top_nodes
            # result[0][0] => Node
            result = {'title': page.title, 'nodes': page.top_nodes, 'url': page.url}
            results.append(result)

        # results[0]['title'] => page.title
        return results

    def search_30_pages(self):
        search_engine = SearchEngine()
        pages = search_engine.google_search(QUERY, 3)
        return pages


if __name__ == '__main__':
    lc = LocalController()
    results = lc.search_and_fetch_headers()
    # いまいるディレクトリにgardeningディテクトリ作って移動
    if not os.path.exists('fetched_pages'):
        os.mkdir('fetched_pages')
    os.chdir('fetched_pages')
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    os.chdir(DIR)
    for i, result in enumerate(results):
        f = open(DIR + '_obj_' + str(i), 'wb')
        pickle.dump(result, f)
        f.close()