# -*- coding: utf-8 -*-
import re
from block import Block
import pdb


class Node():
    def __init__(self, text, heading_type):
        self.html_body = text  # ノード内のすべてのhtml
        self.heading_type = heading_type  # 'h1' or 'h2' or ...
        splitted_texts = re.split('<h', text)
        if len(splitted_texts) > 1:
            self.this_html_body = '<h' + splitted_texts[1]
        else:
            self.this_html_body = text
        self.block = Block(self.this_html_body)

    def set_heading_title(self, title):
        img_pattern = re.compile('<(img|IMG)')
        img_match = img_pattern.search(title)
        if img_match:
            alt_pattern = re.compile('alt=".*?"')
            alt_match = alt_pattern.search(title)
            if alt_match:
                self.heading_title = alt_match.group()[5:-1]  # alt="と"を削除
                return
            else:
                self.heading_title = 'image'
                return
        self.heading_title = title

    def hasattr(self, string):
        if hasattr(self, string):
            return True
        return False

    # いきなりh3,h5となるときは、page.h1_nodes.children[0] => いきなりh3が入っている
    def set_descendants(self):
        """
        # self.textとself.heading_title, self.heading_typeはある
        # 再帰的にself.childrenを作る

        """
        if self.html_body == '':
            return
        # まずliを見つけてセットする
        if '<li>' in self.this_html_body:
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
            if 'の他の記事<' in heading:
                continue
            if '> はじめに<' in heading:
                continue
            if '> おわりに<' in heading:
                continue
            node = Node(html_texts_divided_by_heading[i], children_heading_type)
            node.set_heading_title(heading[4:-5].strip())  # <h2>..</h2>のタグ除去
            node.set_descendants()  # 再帰的に子供を作る
            nodes.append(node)
        return nodes

    def children_heading_info(self, heading_type):
        children_heading_type = 'h' + str(int(heading_type[1]) + 1)
        heading_pattern = re.compile('<%s.*?>.*?</%s>' % (children_heading_type, children_heading_type))
        html_texts_divided_by_heading = heading_pattern.split(self.html_body)[1:]
        headings = heading_pattern.findall(self.html_body)
        return [children_heading_type, html_texts_divided_by_heading, headings]

    def set_li_texts(self):
        li_pattern = re.compile('<li>.*?</li>')
        li_texts_with_tags = li_pattern.findall(self.this_html_body)
        li_texts = []
        for li_text_with_tag in li_texts_with_tags:
            if '<aside' in li_text_with_tag:
                continue
            if '<a href="http://b.hatena' in li_text_with_tag:
                continue
            if '&nbsp' in li_text_with_tag:
                continue
            li_texts.append(self.remove_tags(li_text_with_tag[4:-5]))
        self.li_texts = li_texts

    def remove_tags(self, text):
        tag_pattern = re.compile('<.*?>')
        result = tag_pattern.sub('', text)
        return result