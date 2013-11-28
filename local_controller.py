from search_engine import SearchEngine
import pickle

QUERY = '家庭菜園　始める　方法'


class LocalController():
    def search_and_fetch_headers(self):
        pages = self.search_10_pages()
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

    def search_10_pages(self):
        search_engine = SearchEngine()
        pages = search_engine.google_search(QUERY, 1)
        return pages


if __name__ == '__main__':
    lc = LocalController()
    results = lc.search_and_fetch_headers()
    for result in results:
        f = open(result['title'], 'wb', encoding='UTF-8')
        pickle.dump(result, f)
        f.close()