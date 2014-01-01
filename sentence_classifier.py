# -*- coding: utf-8 -*-
import pdb


class SentenceClassifier():
    """
    文字列でのマッチングだけでは無理なのでめんどいけどmecabでのマッチングもする

    ください        動詞,非自立,*,*,五段・ラ行特殊,命令ｉ,くださる,クダサイ,クダサイ

    下さい  動詞,非自立,*,*,五段・ラ行特殊,命令ｉ,下さる,クダサイ,クダサイ


    ましょ  助動詞,*,*,*,特殊・マス,未然ウ接続,ます,マショ,マショ
    う      助動詞,*,*,*,不変化型,基本形,う,ウ,ウ

    なさい  動詞,非自立,*,*,五段・ラ行特殊,命令ｉ,なさる,ナサイ,ナサイ

    しよ    動詞,自立,*,*,サ変・スル,未然ウ接続,する,シヨ,シヨ
    う      助動詞,*,*,*,不変化型,基本形,う,ウ,ウ

    べき    助動詞,*,*,*,文語・ベシ,体言接続,べし,ベキ,ベキ

    と      助詞,格助詞,引用,*,*,*,と,ト,ト
    いい    動詞,自立,*,*,五段・ワ行促音便,連用形,いう,イイ,イイ

    と      助詞,接続助詞,*,*,*,*,と,ト,ト
    よい    形容詞,非自立,*,*,形容詞・アウオ段,基本形,よい,ヨイ,ヨイ

    と      助詞,接続助詞,*,*,*,*,と,ト,ト
    良い    形容詞,非自立,*,*,形容詞・アウオ段,基本形,良い,ヨイ,ヨイ

    必要    名詞,形容動詞語幹,*,*,*,*,必要,ヒツヨウ,ヒツヨー
    が      助詞,格助詞,一般,*,*,*,が,ガ,ガ

    て      助詞,接続助詞,*,*,*,*,て,テ,テ
    は      助詞,係助詞,*,*,*,*,は,ハ,ワ

    """
    def __init__(self, sentence):
        """
        sentenceはSentenceオブジェクト
        """
        self.m_body_words = sentence.m_body_words

    def direction_r_i(self):
        result_1 = self.cleared_one_hurdle_problem_r_i()
        if result_1:
            return result_1
        result_2 = self.cleared_two_hurdle_problem_r_i()
        if result_2:
            return result_2
        return False

    def one_hurdle_problem_word_infos(self):
        prob_1 = 'ください\t動詞,非自立,*,*,五段・ラ行特殊,命令ｉ,くださる,クダサイ,クダサイ'
        prob_2 = '下さい\t動詞,非自立,*,*,五段・ラ行特殊,命令ｉ,下さる,クダサイ,クダサイ'
        prob_3 = 'なさい\t動詞,非自立,*,*,五段・ラ行特殊,命令ｉ,なさる,ナサイ,ナサイ'
        prob_4 = 'べき\t助動詞,*,*,*,文語・ベシ,体言接続,べし,ベキ,ベキ'
        return [prob_1, prob_2, prob_3, prob_4]

    def two_hurdle_problem_word_infos(self):
        prob_1_1 = 'ましょ\t助動詞,*,*,*,特殊・マス,未然ウ接続,ます,マショ,マショ'
        prob_1_2 = 'う\t助動詞,*,*,*,不変化型,基本形,う,ウ,ウ'

        prob_2_1 = 'しよ\t動詞,自立,*,*,サ変・スル,未然ウ接続,する,シヨ,シヨ'
        prob_2_2 = 'う\t助動詞,*,*,*,不変化型,基本形,う,ウ,ウ'

        prob_3_1 = 'と\t助詞,格助詞,引用,*,*,*,と,ト,ト'
        prob_3_2 = 'いい\t動詞,自立,*,*,五段・ワ行促音便,連用形,いう,イイ,イイ'

        prob_4_1 = 'と\t助詞,接続助詞,*,*,*,*,と,ト,ト'
        prob_4_2 = 'よい\t形容詞,非自立,*,*,形容詞・アウオ段,基本形,よい,ヨイ,ヨイ'

        prob_5_1 = 'と\t助詞,接続助詞,*,*,*,*,と,ト,ト'
        prob_5_2 = '良い\t形容詞,非自立,*,*,形容詞・アウオ段,基本形,良い,ヨイ,ヨイ'

        prob_6_1 = '必要\t名詞,形容動詞語幹,*,*,*,*,必要,ヒツヨウ,ヒツヨー'
        prob_6_2 = 'が\t助詞,格助詞,一般,*,*,*,が,ガ,ガ'

        prob_7_1 = 'て\t助詞,接続助詞,*,*,*,*,て,テ,テ'
        prob_7_2 = 'は\t助詞,係助詞,*,*,*,*,は,ハ,ワ'

        return [[prob_1_1, prob_1_2],
                [prob_2_1, prob_2_2],
                [prob_3_1, prob_3_2],
                [prob_4_1, prob_4_2],
                [prob_5_1, prob_5_2],
                [prob_6_1, prob_6_2],
                [prob_7_1, prob_7_2]]

    def cleared_one_hurdle_problem_r_i(self):
        """
        self.m_body_wordsを見て、1つハードルの問題を突破できるか調べる。
        突破できればそのindexを、できなければFalseを返す
        こっちはreversedが楽。
        """
        for i, m_word in enumerate(reversed(self.m_body_words)):
            for direction_info in self.one_hurdle_problem_word_infos():
                if m_word.word_info == direction_info:
                    return i
        return False

    def cleared_two_hurdle_problem_r_i(self):
        """
        2つハードルの問題をクリアできたらその前半のindexを、
        クリアできなかったらFalseを返す
        """
        for i, m_word in enumerate(reversed(self.m_body_words)):
            for direction_infos in self.two_hurdle_problem_word_infos():
                if m_word.word_info == direction_infos[0]:
                    if self.m_body_words[-i].word_info == direction_infos[1]:
                        return i
        return False
