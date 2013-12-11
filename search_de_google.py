from search_engine import SearchEngine

if __name__ == '__main__':
    query = '花粉症対策'
    engine = SearchEngine()
    pages = engine.google_search('"' + 'で' + query + '"', 3)
    for page in pages:
        try:
            i = page.title.index('で' + query)
            print(page.title[(i - 10):])
        except ValueError:
            try:
                i = page.snippet.index('で' + query)
                print(page.snippet[(i - 10):])
            except:
                pass
