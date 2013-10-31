# -*- coding: utf-8 -*-
import re
import pdb

class Node():
    def __init__(self, text, header_type):
        self.html_body = text  # ノード内のすべてのhtml
        self.header_type = header_type  # 'h1' or 'h2' or ...

    def set_header_title(self, title):
        self.header_title = title

    # いきなりh3,h5となるときは、page.h1_nodes.children[0] => いきなりh3が入っている
    def set_descendants(self):
        """
        # self.textとself.header_title, self.header_typeはある
        # 再帰的にself.childrenを作る

        """
        if self.header_type == 'h6':
            return
        else:
            # headersがないとき、さらに下位を探る
            header_type = self.header_type

            while True:
                children_header_type, html_texts_divided_by_header, headers = \
                    self.calc_header_info(header_type)
                if not headers == []:
                    break
                if header_type == 'h5':  # h5の子供h6。最後。あとはない
                    break
                # self.childrenの準備をheader_type上げておこなう
                header_type = 'h' + str(int(header_type[1]) + 1)
            # header_typeはもう使わない

            # self.childrenを作る
            nodes = []
            for i, header in enumerate(headers):
                node = Node(html_texts_divided_by_header[i + 1], children_header_type)
                node.set_header_title(header[4:-5])  # <h2>..</h2>のタグ除去
                node.set_descendants()
                nodes.append(node)
            self.children = nodes

    def calc_header_info(self, header_type):
        children_header_type = 'h' + str(int(header_type[1]) + 1)
        header_pattern = re.compile('<%s>.*?</%s>' % (children_header_type, children_header_type))
        html_texts_divided_by_header = header_pattern.split(self.html_body)
        headers = header_pattern.findall(self.html_body)
        return [children_header_type, html_texts_divided_by_header, headers]
