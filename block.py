import re
from paragraph import Paragraph

class Block():
    '''
    htmlのh1からh6で区切られた領域
    '''
    def __init__(self, raw_html):
        self.build_paragraphs(raw_html)

    def build_paragraphs(self, html):
        p_htmls = self.to_paragraph_htmls(html)
        self.paragraphs = [Paragraph(p_html) for p_html in p_htmls]

    def to_paragraph_htmls(self, html):
        splitted_by_p = self.split_by_p(html)
        paragraph_htmls = []
        for html_part in splitted_by_p:
            splitted_by_br = self.split_by_br(html_part)
            if not splitted_by_br == '':
                paragraph_htmls.extend(splitted_by_br)
        return paragraph_htmls

    # pやbrがあるにせよないにせよlistを返す
    def split_by_something(self, html, word):
        if word in html:
            return html.split(word)
        return [html]

    def split_by_p(self, html):
        results = self.split_by_something(html, '<p')
        return results

    def split_by_br(self, html):
        results = self.split_by_something(html, '<br')
        return results


