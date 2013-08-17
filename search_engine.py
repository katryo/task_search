import urllib
import urllib.request
import urllib.parse
import json
import pdb
import my_keys
import requests
import constants
from web_page import WebPage


class SearchEngine:
    def __init__(self):
        self.microsoft_api_key = my_keys.MICROSOFT_API_KEY
        self.google_api_key = my_keys.GOOGLE_API_KEY
        self.result_pages = []

    def set_actual_query(self):
        self.actual_query = '%s "%sと" -%sとは' % (self.hint_word, self.action_word, self.action_word)

    def set_solr_query(self):
        self.solr_query = '%s+%sと-%sとは' % (self.hint_word, self.action_word, self.action_word)

    def find_related_action_words(self):
        self.set_actual_query()
        self.material_pages = self.google_search(self.actual_query, 5)
        self.find_pages_including_related_words()

    def find_pages_including_related_words(self):
        for page in self.material_pages:
            for text in [page.title, page.snippet]:
                self.add_to_results_if_key_phrase_present(text, page)

    def find_related_action_words_from_clueweb(self):
        self.set_solr_query()
        texts = self.clue_web_search(self.solr_query)
        for text in texts:
            self.add_to_results_if_key_phrase_present(text, page)


    def add_to_results_if_key_phrase_present(self, text, page):
        start_index = text.find(self.action_word + 'と')
        if start_index > -1:
            self.to_m_words_and_append_to_results(text, start_index, page)

    def to_m_words_and_append_to_results(self, text, start_index, page):
        possible_related_word_index = start_index + len(self.action_word) + 1
        possible_to_include_action_word = text[possible_related_word_index: possible_related_word_index + 10]
        m_words = page.to_m_words(possible_to_include_action_word)
        if len(m_words) > 0:
            self.append_to_result_pages_if_sahen(m_words, page)

    def append_to_result_pages_if_sahen(self, m_words, page):
        if m_words[0].subtype == 'サ変接続' or m_words[0].type == '名詞':
            if len(m_words) > 1:
                if m_words[1].type == '名詞':
                    page.action_word = m_words[0].name + m_words[1].name
                    self.result_pages.append(page)
                else:
                    page.action_word = m_words[0].name
                    self.result_pages.append(page)
            else:
                page.action_word = m_words[0].name
                self.result_pages.append(page)

    def count_action_words(self):
        pages = self.result_pages
        self.action_words_count = {}
        for page in pages:
            if page.action_word in self.action_words_count:
                self.action_words_count[page.action_word] += 1
            else:
                self.action_words_count[page.action_word] = 1
        # self.action_words_count => {'廃車': 3, '買い取り': 5}

    def sort_action_words_count(self):
        self.sorted_action_words = []
        for key, value in sorted(self.action_words_count.items(), key=lambda x:x[1], reverse=True):
            self.sorted_action_words.append({'word': key, 'count': value})

    def clue_web_search(self, query):
        options = '&rows=20'
        url = constants.CLUE_WEB_URL_HEAD + query + options + constants.CLUE_WEB_URL_TAIL
        clue_web_result_page = WebPage(url)
        clue_web_result_page.fetch_xml()
        clue_web_result_page.pick_texts()
        return clue_web_result_page.texts


    def google_search(self, query, num):
        NUM = num
        url = 'https://www.googleapis.com/customsearch/v1?'
        params = {
            'key': self.google_api_key,
            'q': query,
            'cx': '013036536707430787589:_pqjad5hr1a',
            'alt': 'json',
            'lr': 'lang_ja',
        }
        start = 1
        items = []

        for i in range(0, NUM):
            params['start'] = start
            request_url = url + urllib.parse.urlencode(params)
            try:
                response = urllib.request.urlopen(request_url)
                json_body = json.loads(response.read().decode('utf-8'))
                items.extend(json_body['items'])
                if not 'nextPage' in json_body['queries']:
                    break
                start = json_body['queries']['nextPage'][0]['startIndex']
            except:
                items.extend({'link': '#', 'title': '検索できませんでした'})
                 #items => [{'link': 'http://...', 'title': 'ページは'}, {...}...]
        pages = []
        for item in items:
            page = WebPage(item['link'])
            page.title = item['title']
            page.snippet = item['snippet']
            pages.append(page)
        return pages 

    def bing_search(self, query, num):
        NUM = num
        key = self.microsoft_api_key
        url = 'https://api.datamarket.azure.com/Bing/Search/Web?'
        json_param = '&$format=json'
        param = {
            'Query': "'" + query + "'",
        }
        req_url = url + urllib.parse.urlencode(param)
        items = []
        for i in range(0, NUM):
            try:
                json_body = requests.get(req_url + json_param, auth=(key, key)).json()
                items.extend(json_body['d']['results'])
                req_url = json_body['d']['__next']
            except:
                items.extend({'Url': '#', 'Title': '検索できませんでした'})
        pages = []
        for item in items:
            page = WebPage(item['Url'])
            #googleの書き方に統一
            page.title = item['Title']
            page.snippet = item['Description']
            pages.append(page)
        return pages
