# -*- coding: utf-8 -*-
import unittest
from block import Block
import pdb


class TestBlock(unittest.TestCase):

    def setUp(self):
        self.nanapi_block_html = '''<p class="image-block"><a href="?layout=image&amp;url=http%3A%2F%2Fp.nanapi.jp%2Fr%2F20101115%2F20101115163715.jpg"><img src="http://p.cdnanapi.com/r/20101115/20101115163715.jpg" /></a></p>
<p>しょうがはすりおろしたものを使用するのがオススメです。</p>
<p>毎回すりおろすのは手間になりますので、市販のチューブ状のものを利用すると良いでしょう。</p>
<p>尚、しょうがの香りや風味が苦手・・という方にはスライスから試してみるのも良いですよ。比較的しょうがの辛味や香りが抑えられます。</p>
        '''

    def test_init(self):
        b = Block(self.nanapi_block_html)
        self.assertEqual(b.paragraphs[2].sentences[0], 'しょうがはすりおろしたものを使用するのがオススメです')
        self.assertEqual(b.paragraphs[3].sentences[0], '毎回すりおろすのは手間になりますので、市販のチューブ状のものを利用すると良いでしょう')
        self.assertEqual(b.paragraphs[4].sentences[0], '尚、しょうがの香りや風味が苦手・・という方にはスライスから試してみるのも良いですよ')
        self.assertEqual(b.paragraphs[4].sentences[1], '比較的しょうがの辛味や香りが抑えられます')

if __name__ == '__main__':
    unittest.main()