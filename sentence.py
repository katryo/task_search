# -*- coding: utf-8 -*-
from labelable import Labelable
import constants
import re
import pdb
import CaboCha
from sentence_classifier import SentenceClassifier
from text_combiner import TextCombiner


class Sentence(Labelable):
    def __init__(self, text, query):
        super().__init__(text)
        self._set_m_body_words_by_combine_words()
        self.query = query

    def _set_m_body_words_by_combine_words(self):
        tc = TextCombiner()
        m_body_words = tc.combine_nouns(self.m_body_words)
        self.m_body_words = tc.combine_verbs(m_body_words)

    def _core_object(self):
        before_cmp = self._m_words_before_cmp()
        try:
            last_m = before_cmp[-1]
        # を理解していきましょう のように、をの前がないとき
        except IndexError:
            return ''
        if last_m.is_pronoun():
            return 'pronoun'
        try:  # before_woが少ないかも
            before_last_m = before_cmp[-2]
            if before_last_m.name == 'の':
                #  'その階で金の剣を売ってください'は「金の剣を売る」になるべき
                before_no = before_cmp[-3].name
                #  '夏野菜へのシフトをスタートさせましょう'は「夏野菜へのシフトをスタート」になるべき
                if before_no == 'へ':
                    before_before_no = before_cmp[-4].name
                    return before_before_no + 'への' + last_m.name

                #  'その階で金の剣を売ってください'はここに来る
                return before_no + 'の' + last_m.name

            if last_m.name == 'ましょ':
                pdb.set_trace()
            return last_m.name
        except IndexError:  # len(before_wo)が小さいときはここに来る
            return last_m.name

    def _core_predicate(self):
        m_words_after_cmp = self.m_words_after_cmp()
        for i, m_word in enumerate(m_words_after_cmp):
            if m_word.type == '動詞':
                # 例 '運動しましょう'
                if 'サ変' in m_word.word_info and m_words_after_cmp[i-1].type == '名詞':
                    return m_words_after_cmp[i-1].name + m_word.stem
                if m_word.stem == 'くださる' or m_word.stem == '下さる':
                    # 例 'ご遠慮ください'
                    if m_words_after_cmp[i-1].subtype == 'サ変接続':
                        return m_words_after_cmp[i-1].name + 'する'

                    # 例 ご覧ください
                    if m_words_after_cmp[i-1].subtype == '動詞非自立的':
                        return '見る'

                    # 例 ドライヤーを当ててください
                    if m_words_after_cmp[i-1].name == 'て' and m_words_after_cmp[i-2].type == '動詞':
                        return m_words_after_cmp[i-2].stem

                # 吟味して選ぶようにしましょう => 吟味する
                if m_words_after_cmp[i-1].stem == 'に':
                    if m_words_after_cmp[i-2].stem == 'よう':
                        # 吟味して選ぶようにしましょう => 吟味する
                        if m_words_after_cmp[i-3].type == '動詞':
                            return m_words_after_cmp[i-3].stem
                        if m_words_after_cmp[i-3].stem == 'ない':
                            # 慌てて選ばないようにしましょう
                            if m_words_after_cmp[i-4].type == '動詞':
                                return m_words_after_cmp[i-4].name + 'ない'


                return m_word.stem
        return ''

    def set_noun_verb_if_good_task(self):
        if self._is_invalid_for_task():
            return False
        #  ひらがな・カタカナひともじのときはフィルタ
        pattern = re.compile('^[ぁ-んァ-ン]$')
        noun = self._core_object()

        if not noun:  # ''かも
            return False

        if pattern.match(noun):
            return False

        predicate_term = self._core_predicate()
        if not predicate_term:  # ''かも
            return False
        if predicate_term == '?':
            return False

        if predicate_term in constants.STOPWORDS_OF_WEBPAGE_VERB:
            return False

        if '%s　%s' % (noun, predicate_term) == self.query:
            return False

        self.noun = noun
        self.verb = predicate_term
        return True

    def _is_invalid_for_task(self):
        if self._core_noun_is_block_word():
            return True
        if not self._core_object():
            return True
        if not self._includes_directions():
            return True
        if self._includes_cmp_before_direction():
            return False
        # 〜〜しなさい、といったパーツがないときは、数字から始まる、
        if self._is_step():
            return False
        if self._ends_with_present_tense():
            return False
        return True

    def _is_step(self):
        if self._starts_with_symbol():
            return True
        if self._starts_with_digit():
            return True
        if self._starts_with_step():
            return True
        return False

    def _starts_with_step(self):
        step_texts = 'ステップ step STEP'.split(' ')
        try:
            if self.body[:4] in step_texts:
                return True
            if self.body[:2] == 'その':
                if self.body[2].isnumeric():
                    return True
        except IndexError:
            return False
        return False

    def _starts_with_symbol(self):
        symbols = '・ 〇 ● ○ ◎ ★ ☆'.split(' ')
        if self.body[0] in symbols:
            return True
        return False

    def _starts_with_digit(self):
        if self.body[0].isdigit():
            return True
        return False

    def _ends_with_present_tense(self):
        last_m_word = self.m_body_words[-1]
        if last_m_word.type == '動詞' and last_m_word.c_form == '基本形':
            return True
        if last_m_word.name == 'ます':
            m_word_before_last_word = self.m_body_words[-2]
            if m_word_before_last_word.type == '動詞':
                return True
        return False


    def _core_noun_is_block_word(self):
        blockwords = 'は pronoun さ ため 事 こと など ら ついで で て とき ほう ここ もの ご覧 ごらん'.split(' ')
        for blockword in blockwords:
            if self._core_object() == blockword:
                return True
        return False

    def starts_with_block_word(self):
        blockwords_startswith = 'var listli ビューワソフト JavaScript goo ヤフーGoogle className'.split(' ')
        for blockword in blockwords_startswith:
            if self.core_object().startswith(blockword):
                return True
        return False

    def _includes_cmp_before_direction(self):
        if not self._includes_directions():  # をしなさい がなかったらダメ
            return False
        if not self._cmp_r_i():  # 'を'などがなかったらダメ。次の人。
            return False
        if self._cmp_r_i() > self.direction_r_i():
            return True
        return False

    def _includes_directions(self):
        for direction in constants.DIRECTIONS:
            if direction in self.body:
                return True
        return False

    def _cmp_r_i(self):
        for i, m_body_word in enumerate(reversed(self.m_body_words)):
            for cmp_info in constants.CMP_INFO_LIST:
                if cmp_info == m_body_word.word_info:
                    self.cmp = cmp_info.split(',')[0].split('\t')[0]  # 「を」や「で」
                    return i
            if m_body_word.word_info == constants.CMP_INFO_NI:
                # お早めにお知らせください のときにもここに来る。つまりobjectがない場合。
                try:
                    if not self.m_body_words[-i-2].word_info == constants.CMP_INFO_YO:
                        self.cmp = 'に'
                        return i
                except IndexError:
                    # ['に', '代理登録', 'さ', 'れ', 'ます']
                    return -1
                # 例 選ぶようにしましょうのときは、その前に「AをB」のようなパターンがあるか探す
        # 塗れた畳は劣化しやすいので水が残らないようにしましょう
        return -1

    def direction_r_i(self):
        sc = SentenceClassifier(self)
        return sc.direction_r_i()
        # directionは文字列、woはm_wordでやってたからちょい面倒

    def _m_words_before_cmp(self):
        """
        include_cmpでをがあることを確認してから使ってくれ
        """
        r_index = self._cmp_r_i()
        if r_index == -1:
            return []
        index = - r_index
        results = self.m_body_words[:index-1]
        return results

    def m_words_after_cmp(self):
        r_index = self._cmp_r_i()
        if r_index == -1:
            return []
        index = - r_index
        results = self.m_body_words[index:]
        return results

