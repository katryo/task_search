# -*- coding: utf-8 -*-
import constants
import pdb
from web_item import WebItem
from sentence import Sentence
from sentence_separator import SentenceSeparator
from task import Task
from object_term import ObjectTerm
from hypohype_data_loader import HypoHypeDBDataLoader
from entailment_librarian import EntailmentLibrarian
from page_data_loader import PageDataLoader


class WebPage(WebItem):
    def __init__(self, id = 100, url='unknown', query='', snippet='', rank=1000):
        self.id = id
        self.url = url
        self.query = query
        self._convert_query_from_nv_to_ncv()
        self.snippet = snippet
        self.sentences = []
        self.rank = rank

    def set_rank_from_db(self):
        with PageDataLoader() as loader:
            try:
                rank = loader.rank_with_query_url(self.query, self.url)
            except EOFError:
                print('%sのページないです' % self.url)
                rank = 1000
        self.rank = rank

    def _set_subtypes(self):
        self.subtypes = self._subtypes()

    def _subtypes(self):
        """
        nounの下位語を探している。
        """
        if not hasattr(self, 'query_noun'):
            self._convert_query_from_nv_to_ncv()
        subtypes = {}
        with HypoHypeDBDataLoader() as loader:
            subtype_nouns = loader.select_hypos_with_hype(self.query_noun)

        for i, sentence in enumerate(self.sentences):
            for noun in subtype_nouns:
                if noun in sentence.body:
                    subtypes[noun] = i
        return subtypes  # {'シャワールーム': 12, 'トイレ': 93, ...}

    def _subtype_verbs(self):
        """
        とりあえずは使わない。nounだけでsubtypeは十分と判断。
        """
        librarian = EntailmentLibrarian()
        return librarian.entailed_from_all_dictionaries_with_entailing(self.query_verb)

    def _convert_query_from_nv_to_ncv(self):
        words = self.query.split('　')
        if len(words) == 2:
            self.query_noun = words[0]
            self.query_cmp = 'を'
            self.query_verb = words[1]
        elif len(words) == 3 or len(words) == 4:
            self.query_noun = words[0]
            self.query_cmp = words[1]
            self.query_verb = words[2]

    def set_sentences_from_text(self):
        sp = SentenceSeparator(self.text)
        sentence_texts = sp.split_by_dots()
        for sentence_text in sentence_texts:
            sentence = Sentence(sentence_text, self.query)
            self.sentences.append(sentence)

    def set_tasks_from_sentences(self):
        tasks = self._obj_and_predicate_dict_by_wo_from_sentences()
        # ここでもし1ページ内に複数のtaskがあったら、各タスクにbeforeとafterの
        # エッジを与える
        self.tasks = tasks

    def is_shopping(self):
        for sentence in self.sentences:
            for clue in constants.CLUES_FOR_SHOPPING_PAGE:
                if clue in sentence.body:
                    return True
        return False

    def is_official(self):
        for sentence in self.sentences:
            for clue in constants.CLUES_FOR_OFFICIAL_PAGE:
                if clue in sentence.body:
                    return True
        return False

    def _obj_and_predicate_dict_by_wo_from_sentences(self):
        """
        self.sentencesから、「〜〜を〜〜」を見つけて、「AをB」にして返す
        最後に計算する際、同じページでの登場番号の前後で。part-ofを判断する
        """
        results = []
        order = 0
        self._set_subtypes()
        for i, sentence in enumerate(self.sentences):
            if type(sentence) == str:
                sentence = Sentence(text=sentence, query=self.query)

            if not sentence.set_noun_verb_if_good_task():
                continue

            object_term = ObjectTerm(sentence.noun)
            if object_term == 'ましょ':
                pdb.set_trace()

            if object_term.core_noun in constants.STOPWORDS_OF_WEBPAGE_NOUN:
                continue

            distance_between_subtypes = {}
            for subtype in self.subtypes:
                distance = self._distance_between_subtype(i, subtype=subtype)
                distance_between_subtypes[subtype] = distance

            task = Task(object_term=object_term.name,
                        cmp=sentence.cmp,
                        predicate_term=sentence.verb,
                        distance_between_subtypes=distance_between_subtypes,
                        query=self.query,
                        order=order,
                        url=self.url,
                        is_shopping=False,
                        is_official=False,
                        rank=self.rank,
                        sentence=sentence.body)
            results.append(task)
            print('%s_%s_%sというタスクをセットしました' % (sentence.noun, sentence.cmp, sentence.verb))
            order += 1 # 登場の順番
        return results

    def _distance_between_subtype(self, i, subtype):
        # subtype記述がないときは、default_distance_between_task_and_subtypeが与えられる。
        if not subtype in self.subtypes:
            return constants.DEFAULT_DISTANCE_BETWEEN_TASK_AND_SUBTYPE

        subtype_i = self.subtypes[subtype]
        return i - subtype_i


