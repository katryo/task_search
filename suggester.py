import requests
from lxml import etree
URL_HEAD = 'http://google.com/complete/search?hl=ja&output=toolbar&q='
QUERY = 'アルバイト 始める'


class Suggester():
    def suggest_with_query(self, query):
        self.set_query(query)
        self.create_tree()
        self.parse_suggestions()

    def fetch_xml(self):
        url = URL_HEAD + self.query
        response = requests.get(url)
        return response.text

    def create_tree(self):
        text = self.fetch_xml()
        self.root = etree.fromstring(text)

    def parse_suggestions(self):
        self.create_tree()
        suggestions = []
        for suggestion in self.root:
            new_word = suggestion[0].values()[0]
            if new_word:
                suggestions.append(new_word)
        self.suggestions = suggestions

    def set_query(self, query):
        self.query = query

if __name__ == '__main__':
    suggester = Suggester()
    suggester.suggest_with_query(QUERY)
    for suggestion in suggester.suggestions:
        print(suggestion)