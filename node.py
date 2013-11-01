# -*- coding: utf-8 -*-
import re
from lxml import html
import pdb


class Node():
    def __init__(self, text, heading_type):
        self.html_body = text  # ノード内のすべてのhtml
        self.heading_type = heading_type  # 'h1' or 'h2' or ...
        splited_texts = re.split('<h', text)
        if len(splited_texts) > 1:
            self.this_html_body = '<h' + splited_texts[1]
            return
        self.this_html_body = text

    def set_heading_title(self, title):
        self.heading_title = title

    # いきなりh3,h5となるときは、page.h1_nodes.children[0] => いきなりh3が入っている
    def set_descendants(self):
        """
        # self.textとself.heading_title, self.heading_typeはある
        # 再帰的にself.childrenを作る

        """
        if self.html_body == '':
            return
        # まずliを見つけてセットする
        self.set_li_texts()
        # h6ノードはその下位ノードを作る必要ない
        if self.heading_type == 'h6':
            return

        heading_type = self.heading_type
        while True:
            children_heading_type, html_texts_divided_by_heading, headings = \
                self.children_heading_info(heading_type)
            if not headings == []:
                break
            if heading_type == 'h5':  # h5の子供h6。最後。あとはない
                break
            # self.childrenの準備をheading_type上げておこなう
            heading_type = 'h' + str(int(heading_type[1]) + 1)
        # heading_typeはもう使わない

        # self.childrenを作る
        self.children = self.build_children(headings, html_texts_divided_by_heading, children_heading_type)

    def build_children(self, headings, html_texts_divided_by_heading, children_heading_type):
        nodes = []
        for i, heading in enumerate(headings):
            node = Node(html_texts_divided_by_heading[i], children_heading_type)
            node.set_heading_title(heading[4:-5].strip())  # <h2>..</h2>のタグ除去
            node.set_descendants()  # 再帰的に子供を作る
            nodes.append(node)
        return nodes

    def children_heading_info(self, heading_type):
        children_heading_type = 'h' + str(int(heading_type[1]) + 1)
        heading_pattern = re.compile('<%s>.*?</%s>' % (children_heading_type, children_heading_type))
        html_texts_divided_by_heading = heading_pattern.split(self.html_body)[1:]
        headings = heading_pattern.findall(self.html_body)
        return [children_heading_type, html_texts_divided_by_heading, headings]

    def set_li_texts(self):
        if self.this_html_body == '':
            return
        # http://stackoverflow.com/questions/10165756/html-parsing-with-lxml-when-theres-no-root-tag
        fragments = html.fromstring(self.this_html_body)
        if len(fragments) == 0:
            return
        if isinstance(fragments[0], str):
            return
        li_elements = fragments[0].xpath('//li')
        li_texts = []
        for li_elem in li_elements:
            li_texts.append(li_elem.text)
        self.li_texts = li_texts