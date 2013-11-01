# -*- coding: utf-8 -*-
from node import Node


class NodeFactory():
    def __init__(self, html_texts, children_heading_type):
        self.html_texts = html_texts
        self.children_heading_type = children_heading_type

    def product_nodes(self):
        nodes = []
        for i, heading in enumerate(self.headings):
            node = Node(self.html_texts_divided_by_heading[i], self.children_heading_type)
            node.set_heading_title(heading[4:-5])  # <h2>..</h2>のタグ除去
            node.set_descendants()
            nodes.append(node)
        return nodes



