# -*- coding: utf-8 -*-
import constants
import MeCab
from m_words_factory import MWordsFactory


class SentenceSeparator():
    def __init__(self, text):
        self.text = text

    def split_by_dots(self):
        """
        再帰的にsplitして1つのlistにする
        """
        texts = self.split_texts_by_dots([self.text])
        # dotで繰り返しているのが話をややこしくしている。
        return texts

    def split_texts_by_dots(self, texts):
        for dot in constants.DOTS:
            # 問題は、strとlistの型の違い
            # split_by_dotsはstrで入ってlistを返すのでそのまま再帰で使えない
            # listで入ってlistを返す関数があればいい
            # ['a。aaaa', 'bbb。bbbb', 'cccc.cc!cc']など、ひとまず'。'でsplitする
            texts = self.split_and_flatten_by_a_certain_dot(texts, dot)
        return texts

    def split_and_flatten_by_a_certain_dot(self, texts, dot):
        """
        listを入れてlistを返す
        """
        # 最初は['あいう。えお！かき。くけこ']
        results = []
        for text in texts:
            # まず。がある
            splitted_texts = text.split(dot)
            for splitted_text in splitted_texts:
                if splitted_text:
                    # splitted_textsは['あいう', 'えお！かき', 'くけこ']
                    results.append(splitted_text)
        return results

    def sahens_or_verbs(self, text):
        s_list = self.sahens(text)
        v_list = self.verbs(text)
        return s_list + v_list

    def sahens(self, text):
        keywords = []
        m_words_factory = MWordsFactory()
        mwords = m_words_factory.build_from(text)
        for m_word in mwords:
            if m_word.subtype == 'サ変接続':
                item = m_word.name
                keywords.append(item)
        return keywords

    def verbs(self, text):
        keywords = []
        m_words_factory = MWordsFactory()
        mwords = m_words_factory.build_from(text)
        for m_word in mwords:
            if m_word.type == '動詞':
                item = m_word.stem
                keywords.append(item)
        return keywords


    def _split_to_words(self, text, to_stem=False):
        """
        入力: 'すべて自分のほうへ'
        出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
        """
        tagger = MeCab.Tagger('mecabrc')  # 別のTaggerを使ってもいい
        mecab_result = tagger.parse(text)
        info_of_words = mecab_result.split('\n')
        words = []
        for info in info_of_words:
            # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
            if info == 'EOS' or info == '':
                break
                # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
            info_elems = info.split(',')
            # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
            if info_elems[6] == '*':
                # info_elems[0] => 'ヴァンロッサム\t名詞'
                words.append(info_elems[0][:-3])
                continue
            if to_stem:
                # 語幹に変換
                words.append(info_elems[6])
                continue
                # 語をそのまま
            words.append(info_elems[0][:-3])
        return words

    def words(self, text):
        words = self._split_to_words(text, to_stem=False)
        return words

    def stems(self, text):
        stems = self._split_to_words(text, to_stem=True)
        return stems

    def target_from_m_words_and_wo_i(self, m_words, wo_i):
        targets = m_words[:wo_i]
        for m_word in reversed(targets):
            if m_word.type == '名詞':
                return m_word.name
        return '?'

    def action_from_m_words_and_wo_i(self, m_words, wo_i):
        action_like_m_words = m_words[wo_i:]
        for i, m_word in enumerate(action_like_m_words):
            if m_word.type == '動詞':
                if 'サ変接続' in action_like_m_words[i-1].word_info:
                    return action_like_m_words[i-1].stem
                return m_word.stem
        return '?'

