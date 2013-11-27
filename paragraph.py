import re
from web_item import WebItem


class Paragraph(WebItem):
    '''
    <p>か<br/>で囲まれた部分。self.sentencesを持つ
    '''
    def __init__(self, html):
        self.sentences = self.to_sentences(html)

    def to_sentences(self, html):
        '''
        htmlを.や。で分割して..>aaaa<tag>bbbb<..などのいらない部分を除去する
        '''
        noisy_sentences = self.split_by_dots(html)
        sentences = []
        for noisy_sentence in noisy_sentences:
            sentence = self.remove_tags(noisy_sentence)
            if sentence and sentence != '\n':
                sentences.append(sentence)
        return sentences

    def split_by_dots(self, html):
        html_items = [html]
        for dot in ['。', '！', '？']:
            html_items_in_items = [html_item.split(dot) for html_item in html_items]
            html_results = []
            for html_items_in_item in html_items_in_items:
                html_results.extend(html_items_in_item)
            html_items = html_results
        return html_items

