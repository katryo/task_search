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
        self.assertEqual(h1_node.children[0].header_type, 'h2')
        self.assertEqual(h1_node.children[0].header_title, 'cccc')
        self.assertEqual(len(h1_node.children), 1)

    def test_set_descendants_with_h1_and_h2(self):
        h1_node = Node('<html>a<h2>header1</h2>b<h2>header2</h2>c</html>', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].html_body, 'b')
        self.assertEqual(h1_node.children[0].header_type, 'h2')
        self.assertEqual(h1_node.children[0].header_title, 'header1')
        self.assertEqual(h1_node.children[1].html_body, 'c</html>')
        self.assertEqual(h1_node.children[1].header_type, 'h2')
        self.assertEqual(h1_node.children[1].header_title, 'header2')
        self.assertEqual(len(h1_node.children), 2)

    def test_set_descendants_with_h1_h2_h3(self):
        h1_node = Node('a<h2>header1</h2>b<h3>smallheader1</h3>c<h2>header2</h2>c<h3>smallheader2</h3>d', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].header_title, 'header1')
        self.assertEqual(h1_node.children[0].children[0].header_title, 'smallheader1')
        self.assertEqual(h1_node.children[1].header_title, 'header2')
        self.assertEqual(h1_node.children[1].children[0].header_title, 'smallheader2')
        self.assertEqual(len(h1_node.children), 2)
        self.assertEqual(len(h1_node.children[0].children), 1)
        self.assertEqual(len(h1_node.children[1].children), 1)

    def test_set_descendants_with_h3_h4_h5(self):
        h1_node = Node('<h3>header3</h3><h4>header4</h4><h5>header5</h5>', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].header_title, 'header3')
        self.assertEqual(h1_node.children[0].children[0].header_title, 'header4')
        self.assertEqual(h1_node.children[0].children[0].children[0].header_title, 'header5')

    def test_set_descendants_with_h3_h5(self):
        h1_node = Node('<h3>header3</h3><h5>header5</h5>', 'h1')
        h1_node.set_descendants()
        self.assertEqual(h1_node.children[0].header_title, 'header3')
        self.assertEqual(h1_node.children[0].children[0].header_title, 'header5')

if __name__ == '__main__':
    unittest.main()