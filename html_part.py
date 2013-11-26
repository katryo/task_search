#  WebPageのHTMLをBlocksやParagraphs, Sentencesにする役目を持つ。
import re


class HtmlPart():
    def __init__(self, html):
        self.raw_html = html

    def build_paragraphs(self):
        #  raw_htmlからpで囲まれているものか<br>, </br>で改行しているものを
        #  取る。つまり、
        if '<p' in self.raw_html:
            self.split_raw_html()

    def raw_html_to_demi_paragraphs(self):
        htmls_splitted_by_p = self.raw_html.split('<p')
        return htmls_splitted_by_p

    def demi_paragraphs_to_paragraphs_with_tags(self, htmls_splitted_by_p):
        #  demi_paragraphはpで
        paragraphs = []
        for html_splitted_by_p in htmls_splitted_by_p:
            if 'br>' in html_splitted_by_p:
                paragraphs.push(html_splitted_by_p.split('br>'))
            else:
                paragraphs.push(html_splitted_by_p)
        return paragraphs

    def clear_inner_tags(self, html):
        pattern = re.compile('<.*?>')
        cleard_text = pattern