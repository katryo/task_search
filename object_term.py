# -*- coding: utf-8 -*-
import pdb
from sentence_separator import SentenceSeparator
from text_combiner import TextCombiner


class ObjectTerm():
    """
    目的語オブジェクト。たいていの場合は名詞。「という検索」により、具体化した語（instance-of関係）や
    抽象化した語（逆instance-of関係）を探せる。
    """
    def __init__(self, text='', context=''):
        self.name = text
        self.context = context  # contextはたいてい検索クエリが入る。

