# -*- coding: utf-8 -*-
import unittest
from node import Node
from web_page import WebPage
import pdb

class TestNode(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_descendants_with_simple_html(self):
        h1_node = Node('bbbbb<h2>cccc</h2>dddd', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].html_body, 'dddd')
        self.assertEqual(h1_node.children[0].heading_type, 'h2')
        self.assertEqual(h1_node.children[0].heading_title, 'cccc')
        self.assertEqual(len(h1_node.children), 1)
        self.naver_hay_fever_page = WebPage('http://matome.naver.jp/topic/1LzuV')

    def test_set_descendants_with_h1_and_h2(self):
        h1_node = Node('<html>a<h2>heading1</h2>b<h2>heading2</h2>c</html>', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].html_body, 'b')
        self.assertEqual(h1_node.children[0].heading_type, 'h2')
        self.assertEqual(h1_node.children[0].heading_title, 'heading1')
        self.assertEqual(h1_node.children[1].html_body, 'c</html>')
        self.assertEqual(h1_node.children[1].heading_type, 'h2')
        self.assertEqual(h1_node.children[1].heading_title, 'heading2')
        self.assertEqual(len(h1_node.children), 2)

    def test_set_descendants_with_h1_h2_h3(self):
        h1_node = Node('a<h2>heading1</h2>b<h3>smallheading1</h3>c<h2>heading2</h2>c<h3>smallheading2</h3>d', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].heading_title, 'heading1')
        self.assertEqual(h1_node.children[0].children[0].heading_title, 'smallheading1')
        self.assertEqual(h1_node.children[1].heading_title, 'heading2')
        self.assertEqual(h1_node.children[1].children[0].heading_title, 'smallheading2')
        self.assertEqual(len(h1_node.children), 2)
        self.assertEqual(len(h1_node.children[0].children), 1)
        self.assertEqual(len(h1_node.children[1].children), 1)

    def test_set_descendants_with_h3_h4_h5(self):
        h1_node = Node('<h3>heading3</h3><h4>heading4</h4><h5>heading5</h5>', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].heading_title, 'heading3')
        self.assertEqual(h1_node.children[0].children[0].heading_title, 'heading4')
        self.assertEqual(h1_node.children[0].children[0].children[0].heading_title, 'heading5')

    def test_set_descendants_with_h3_h5(self):
        h1_node = Node('<h3>heading3</h3><h5>heading5</h5>', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].heading_title, 'heading3')
        self.assertEqual(h1_node.children[0].children[0].heading_title, 'heading5')

    def test_children_heading_info(self):
        node = Node('<h3>heading3</h3><h5>heading5</h5>', 'h1')
        info = node.children_heading_info('h2')
        self.assertEqual(info[0], 'h3')
        self.assertEqual(info[1], ['<h5>heading5</h5>'])
        self.assertEqual(info[2], ['<h3>heading3</h3>'])

    def test_set_li_texts(self):
        node = Node('<ul><li>a</li><li>b</li><li>c</li></ul>', 'h1')
        node.set_li_texts()
        self.assertEqual(node.li_texts, ['a', 'b', 'c'])

    def test_set_li_texts_when_html_is_complicated(self):
        node = Node('<h1>heading1</h1><ul><li>a</li><li>b</li><li>c</li></ul>\
            <h2>heading2</h2><ul><li>d</li><li>e</li><li>f</li></ul>', 'h0')
        node.set_li_texts()
        self.assertEqual(node.li_texts, ['a', 'b', 'c'])

if __name__ == '__main__':
    unittest.main()