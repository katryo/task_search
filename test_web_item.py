# -*- coding: utf-8 -*-
import unittest
from web_item import WebItem
import pdb


class TestWebItem(unittest.TestCase):

    def test_set_text_from_html_body(self):
        html = """
          <tr>
        <td><font face="ＭＳ ゴシック">ですので、掃除をしている私が言うのもなんですが、ホテルに泊まった時の注意事項を！<br>
        （私はホテルに泊まる時は、まず必ずこうしてます）<br>
        <br>
        <br>
        </font></td>
    </tr>
    <tr>
        <td><font face="ＭＳ ゴシック"><strong>１．浴室は使用前に一度、熱湯消毒をしましょう！<br>
        <br>
        １．トイレの便座も一度拭きましょう！<br>
        """
        item = WebItem()
        item.html_body = html
        item.set_text_from_html_body()

if __name__ == '__main__':
    unittest.main()