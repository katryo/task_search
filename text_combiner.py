# -*- coding: utf-8 -*-
from mecabed_noun import MecabedNoun
from mecabed_verb import MecabedVerb
from parenthesis_remover import Parenthesis_remover


class TextCombiner(Parenthesis_remover):
    def combine_verbs(self, m_words):
        new_m_words = self._try_combine_verbs(m_words)
        # 合致するまで=変化しなくなるまで繰り返す
        if new_m_words == m_words:
            return m_words
        else:
            return self.combine_verbs(new_m_words)

    def _try_combine_verbs(self, m_words):
        for i, m_word in enumerate(m_words):
            # 最後の単語は次がないので連続しない
            # m_words == [m_word]のとき i == 0, len(m_words) == 1
            if i + 1 == len(m_words):
                break
                # 名詞を見つけたら、その次の単語が名詞か調べる
            if m_word.subtype == '自立':
                if m_words[i + 1].subtype == '自立':
                    # やった！ 見つけたぞ！
                    # 名詞、名詞のコンボがあれば、m_wordsを再構成する
                    return self._combine_to_one_word(m_words, i, pos='動詞')
        return m_words

    def combine_nouns(self, m_words):
        """
        再帰的に合体させる
        :param m_words:
        :return:
        """
        new_m_words = self._try_combine_nouns(m_words)
        # 合致するまで=変化しなくなるまで繰り返す
        # ただし、20回くらい繰り返したら諦める機能が必要？
        if new_m_words == m_words:
            return m_words
        else:
            return self.combine_nouns(new_m_words)

    def _try_combine_nouns(self, m_words):
        for i, m_word in enumerate(m_words):
            # 最後の単語は次がないので連続しない
            # m_words == [m_word]のとき i == 0, len(m_words) == 1
            if i + 1 == len(m_words):
                break
                # 名詞を見つけたら、その次の単語が名詞か調べる
            if m_word.type == '名詞':
                if m_words[i + 1].type == '名詞':
                    # やった！ 見つけたぞ！
                    # 名詞、名詞のコンボがあれば、m_wordsを再構成する
                    return self._combine_to_one_word(m_words, i, pos='名詞')
        return m_words

    # nounでもverbでも使う
    def _combine_to_one_word(self, m_words, i, pos):
        left_m = m_words[i]
        right_m = m_words[i + 1]
        if pos == '名詞':
            combined_m = MecabedNoun(left_m.name + right_m.name)
        else:
            combined_m = MecabedVerb(left_m.name + right_m.name)
        if i == 0 and len(m_words) == i + 2:
            return [combined_m]
        if i == 0 and len(m_words) != i + 2:
            m_words_after_combine = [combined_m] + m_words[i + 2:]
            return m_words_after_combine
        if i != 0 and len(m_words) == i + 2:
            m_words_after_combine = m_words[:i] + [combined_m]
            return m_words_after_combine
        m_words_after_combine = m_words[:i] + [combined_m] + m_words[i + 2:]
        return m_words_after_combine

