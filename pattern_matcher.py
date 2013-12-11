from search_engine import SearchEngine


class PatternMatcher():
    def __init__(self, query):
        self.query = query
        self.search_num = 2

    def google_search(self):
        engine = SearchEngine()
        pages = engine.google_search(self.query, self.search_num)
        return pages