# -*- coding: utf-8 -*-
import requests
import cchardet
from pyquery import PyQuery as pq
from ad import Ad
from web_item import WebItem
from task import Task
from task_step import TaskStep
from node import Node
import re
import pdb


class WebPage(WebItem):
    def __init__(self, url='unknown'):
        self.url = url

    def fetch_xml(self):
        response = requests.get(self.url)
        self.xml_body = response.text

    # page.build_heading_tree() でツリーを作る。すでにself.htmlはfetchずみ
    def build_heading_tree(self):
        """
        h1
        ul>li
        h2
        h2
        の場合は、……。
        node.lisにセットする
        h1で分けた場合、トップが1つとは限らない。なのでtop_nodesとしている
        self.top_heading_nodes == root; root.heading_title = 'nanapi!!'; root.children == [node1, node2, ...]
        """
        root_node = Node(self.html_body, 'h0')
        root_node.set_descendants()
        self.top_nodes = root_node.children


    # tree = page.heading_tree()
    def heading_tree(self):
        pass

    def set_lines_from_texts(self):
        #result_page単体が実行する
        self.lines = self.text_body.split('。')

    def set_line_clusters_around_action_word(self):
        #result_page単体が実行
        self.line_clusters_around_action_word = []
        sorted_line_nums = sorted(self.line_nums_around_action_word)
        nugget_lines = []
        for i, num in enumerate(sorted_line_nums):
            nugget_lines.append(self.lines[num])
            if num is sorted_line_nums[-1]: # => 最後のそして最大の数字
                self.line_clusters_around_action_word.append(nugget_lines)
                break
            next_num = sorted_line_nums[i + 1]
            if next_num > num + 1:
                self.line_clusters_around_action_word.append(nugget_lines)
                nugget_lines = []
                continue

    def find_lines_with_action_word_from_result_page(self, action_word):
        for result_page in self.result_pages:
            # result_pageはWebPageオブジェクト
            # result_pageは1つのWebページ

            result_page.set_lines_from_texts()
            # result_page.lines => ['aa', 'bb', ...]

            result_page.set_line_nums_with_word(action_word)
            # result_page.line_nums_has_action_word => [3, 8, 12]

    def set_line_nums_around_action_word(self):
        self.line_nums_around_action_word = set([])
        for num in self.line_nums_with_action_word:
            if num == 0: #最初の行にaction_wordがあるとき
                self.line_nums_around_action_word.add(num)
                if len(self.line_nums_with_action_word) is 1:
                    # 1行だけの文章のとき
                    break
                self.line_nums_around_action_word.add(num + 1)
                continue
            elif num == len(self.lines) - 1:
                self.line_nums_around_action_word.add(num - 1)
                self.line_nums_around_action_word.add(num)
                break # linesの最後なので最後であること確定
            else:
                self.line_nums_around_action_word.add(num - 1)
                self.line_nums_around_action_word.add(num)
                self.line_nums_around_action_word.add(num + 1)

    def set_line_nums_with_word(self, word):
        #1つのwebページであるresult_pageが実行する。
        self.line_nums_with_action_word = set([])
        for index, line in enumerate(self.lines):
            if word in line:
                self.line_nums_with_action_word.add(index)

    def pick_texts_to_result_pages(self):
        self.result_pages = set([])
        text_elements = pq(self.xml_body.encode('utf-8')).find('str[name="text"]')
        for elem in text_elements:
            result_page = WebPage('unknown')
            result_page.text_body = elem.text
            self.result_pages.add(result_page)

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


    def find_urls_from_nanapi_search_result(self):
        link_elems = pq(self.html_body.encode('utf-8')).find('.item-title a')
        urls = []
        for link_elem in link_elems:
            url = pq(link_elem).attr('href')
            urls.append(url)
        return urls

    def find_task_from_nanapi_with_headings(self):
        # h2 has_many h3 s
        # self.html_bodyのうち、recipe-bodyを取ってくる
        recipe_body = pq(self.html_body.encode('utf-8')).find('.recipe-body').html()
        # splitして
        steps_texts = recipe_body.split('<h2>')[1:]
        task_steps = []
        for step_text in steps_texts:
            task_step = TaskStep()
            task_step.set_headings_from_text(step_text)
            task_steps.append(task_step)
            # step_text => h2からh2まで
        task = Task()
        task.set_title_with_html(self.html_body)
        task.set_url(self.url)
        task.set_steps(task_steps)
        return task # task.steps => [task_step, task_step, ...]



    def find_tasks_from_texts(self):
        verbs = []
        item = WebItem()
        for line in self.lines:
            mecabed_words = item.to_m_words(line)
            for m_word in mecabed_words:
                if m_word.type == '動詞':
                    verbs.append(m_word)
        return verbs


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

    def pick_key_phrases(self):
        results = pq(self.xml_body.encode('utf-8')).children()
        if not results:
            return []
        key_phrases = []
        for result in results:
            key_phrase = result[0].text
            key_phrases.append(key_phrase)
        return key_phrases

    def fetch_ads(self):
        listWrap = pq(self.html_body).find('.listWrap')
        lis = listWrap.children().children()
        self.ads = []
        for li in lis:
            pq_li = pq(li)
            title = pq_li.find('a').text()
            link = pq_li.find('a').attr('href')
            snippet = pq_li.find('.smr').text()
            ad_info = {'title': title, 'snippet': snippet, 'link': link}
            ad = Ad(ad_info)
            self.ads.append(ad)
