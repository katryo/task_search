import requests
from pyquery import PyQuery as pq
from ad import Ad
from web_item import WebItem


class WebPage(WebItem):
    def __init__(self, url):
        self.url = url

    def fetch_html(self):
        response = requests.get(self.url)
        self.html = response.text

    def fetch_xml(self):
        response = requests.get(self.url)
        self.xml_body = response.text

    def find_action_word(self, action_word):
        snippet_and_title = [self.snippet, self.title]
        for text in snippet_and_title:
            start_index = text.find(action_word + 'と')
            if start_index > -1:
                possible_to_include_action_word = text[start_index + len(action_word) + 1:10]
                m_words = self.to_m_words(possible_to_include_action_word)
                if len(m_words) > 0:
                    if m_words[0].subtype == 'サ変接続':
                        self.action_word = m_words[0]

    def pick_texts(self):
        self.texts = []
        #多目的用途。研究には使わない。自由に書きかえて大丈夫
        text_elements = pq(self.xml_body.encode('utf-8')).find('str[name="text"]')
        for elem in text_elements:
            self.texts.append(elem.text)


    def pick_something(self):
        #多目的用途。研究には使わない。自由に書きかえて大丈夫
        text = pq(self.html).find('td>a>font').text()
        words = text.split(' ')
        normalized_words = []
        for word in words:
            word = word.lower()
            word = word.replace('_', '-')
            word = '"' + word + '",'
            normalized_words.append(word)
        return normalized_words

    def fetch_ads(self):
        nlist = pq(self.html).find('.nlist')
        lis = nlist.children().children()
        ads = []
        for li in lis:
            pq_li = pq(li)
            title = pq_li.find('a').text()
            link = pq_li.find('a').attr('href')
            snippet = pq_li.find('.yschabstr').text()
            ad_info = {'title': title, 'snippet': snippet, 'link': link}
            ad = Ad(ad_info)
            ads.append(ad)
        return ads
