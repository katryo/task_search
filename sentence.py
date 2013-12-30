# -*- coding: utf-8 -*-
from labelable import Labelable
from mecabed_noun import MecabedNoun
import patterns
import constants
import pdb
from sentence_classifier import SentenceClassifier


class Sentence(Labelable):
    def __init__(self, text):
        super().__init__(text)
        self.set_m_body_words_by_combine_nouns()

    def includes_wo_before_direction(self):
        if not self.includes_wo():  # 'を'がなかったらダメ。次の人。
            return False
        if not self.includes_directions():  # をしなさい がなかったらダメ
            return False
        if self.wo_i() < self.direction_i():
            return True
        return False


    def includes_wo(self):
        for m_body_word in self.m_body_words:
            if 'を\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ' in m_body_word.word_info:
                return True
        return False

    def includes_directions(self):
        for direction in patterns.directions:
            if direction in self.body:
                return True
        return False

    def core_obj_and_verb(self):
        return self.core_object() + 'を' + self.core_verb()

    def wo_i(self):
        for i, m_body_word in enumerate(self.m_body_words):
            if 'を\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ' in m_body_word.word_info:
                return i
        raise ValueError

    def direction_i(self):
        sc = SentenceClassifier(self)
        return sc.direction_i()
        # directionは文字列、woはm_wordでやってたからちょい面倒

    def m_words_before_wo(self):
        """
        include_woでをがあることを確認してから使ってくれ
        """
        results = self.m_body_words[:self.wo_i()]
        return results

    def m_words_after_wo(self):
        results = self.m_body_words[self.wo_i()+1:]
        return results

    def core_object(self):
        before_wo = self.m_words_before_wo()
        last_m = before_wo[-1]
        if last_m.is_pronoun():
            return 'pronoun'
        try:  # before_woが少ないかも
            before_last_m = before_wo[-2]
            if before_last_m.name == 'の':
                #  'その階で金の剣を売ってください'は「金の剣を売る」になるべき
                before_no = before_wo[-3].name
                #  '夏野菜へのシフトをスタートさせましょう'は「夏野菜へのシフトをスタート」になるべき
                if before_no == 'へ':
                    before_before_no = before_wo[-4].name
                    return before_before_no + 'への' + last_m.name

                #  'その階で金の剣を売ってください'はここに来る
                return before_no + 'の' + last_m.name
            return last_m.name
        except IndexError:  # len(before_wo)が小さいときはここに来る
            return last_m.name

    def core_verb(self):
        m_words_after_wo = self.m_words_after_wo()
        for i, m_word in enumerate(m_words_after_wo):
            if m_word.type == '動詞':
                # 例 '運動しましょう'
                if 'サ変' in m_word.word_info and m_words_after_wo[i-1].type == '名詞':
                    return m_words_after_wo[i-1].name + m_word.stem
                if m_word.stem == 'くださる' or m_word.stem == '下さる':
                    # 例 'ご遠慮ください'
                    if m_words_after_wo[i-1].subtype == 'サ変接続':
                        return m_words_after_wo[i-1].name + 'する'

                    # 例 ご覧ください
                    if m_words_after_wo[i-1].subtype == '動詞非自立的':
                        return '見る'

                    # 例 ドライヤーを当ててください
                    if m_words_after_wo[i-1].name == 'て' and m_words_after_wo[i-2].type == '動詞':
                        return m_words_after_wo[i-2].stem

                return m_word.stem
        return '?'

    def set_m_body_words_by_combine_nouns(self):
        self.m_body_words = self.combine_nouns(self.m_body_words)

    def combine_nouns(self, m_words):
        """
        再帰的に合体させる
        :param m_words:
        :return:
        """
        new_m_words = self._try_combine_nouns(m_words)
        # 合致するまで=変化しなくなるまで繰り返す
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
                    new_m_words = self._combine_to_one_noun(m_words, i)
                    return new_m_words
        return m_words

    def _combine_to_one_noun(self, m_words, i):
        left_m = m_words[i]
        right_m = m_words[i + 1]
        combined_m = MecabedNoun(left_m.name + right_m.name)
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

