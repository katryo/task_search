# -*- coding: utf-8 -*-
import requests
import constants
import pdb
from pyquery import PyQuery as pq
from web_item import WebItem
from parenthesis_remover import Parenthesis_remover
from sentence import Sentence
from sentence_separator import SentenceSeparator
from task import Task
from node import Node
from object_term import ObjectTerm
from hypohype_data_loader import HypoHypeDBDataLoader
from entailment_librarian import EntailmentLibrarian


class WebPage(WebItem):
    def __init__(self, url='unknown', query='', snippet=''):
        self.url = url
        self.query = query
        self._convert_query_from_nv_to_ncv()
        self.snippet = snippet
        self.sentences = []

    def _subtype_indexes(self):
        """
        nounの下位語を探している。
        """
        if not hasattr(self, 'query_noun'):
            self._convert_query_from_nv_to_ncv()
        indexes = []
        with HypoHypeDBDataLoader() as loader:
            subtype_nouns = loader.select_hypos_with_hype(self.query_noun)

        for i, sentence in enumerate(self.sentences):
            for noun in subtype_nouns:
                if noun in sentence.body:
                    indexes.append(i)
        return indexes

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
        elif len(words) == 3:
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


            distance = self._distance_between_subtype(i)

            task = Task(object_term=object_term,
                        cmp=sentence.cmp,
                        predicate_term=sentence.verb,
                        distance_between_subtype=distance,
                        query=self.query,
                        order=order,
                        url=self.url,
                        is_shopping=self.is_shopping(),
                        is_official=self.is_official())
            results.append(task)
            print('%s_%s_%sというタスクをセットしました' % (sentence.noun, sentence.cmp, sentence.verb))
            order += 1 # 登場の順番
        return results

    def _distance_between_subtype(self, i):
        indexes = self._subtype_indexes()
        # subtype記述がないときは、default_distance_between_task_and_subtypeが与えられる。
        if not indexes:
            return constants.DEFAULT_DISTANCE_BETWEEN_TASK_AND_SUBTYPE

        negative_max = 0
        positive_min = 0
        for index in indexes:
            # subtype記述のある行であれば、0
            if i == index:
                return 0

            # subtype記述のあとのときは正の数字で、最小のもの
            if index < i:
                distance = i - index
                if positive_min > distance:
                    positive_min = distance

            # subtype記述の前のときは、負の数字で、最大のもの
            if index > i:
                distance = i - index # distanceは負
                if negative_max < distance:
                    negative_max = distance

        # 正の距離があるときは正の距離を返す
        # 正の距離がなかったときつまりsubtypeの前がタスクだったときは負の距離を返す

        if positive_min > 0:
            return positive_min
        return negative_max

    def snippet_without_parenthesis(self):
        pr = Parenthesis_remover()
        snippet = pr.remove_inside_round_parenthesis(self.snippet)
        snippet = pr.remove_parenthesis(snippet)
        return snippet

    def fetch_xml(self):
        response = requests.get(self.url)
        self.xml_body = response.text

    def build_keyword(self, query):
        self.keyword = self.from_snippet_to_keyword(query)

    def from_snippet_to_keyword(self, query):
        if query in self.snippet:
            return self.keyword_from_text(self.snippet, query)
        if query in self.title:
            return self.keyword_from_text(self.title, query)
        return ''

    # keywordなのでm_wordsではなくstringにして返す
    def keyword_from_text(self, text, query):
        suspicious_string_size = 20
        i = text.index(query)
        if i < suspicious_string_size:
            suspicious_string = text[:i]
        else:
            suspicious_string = text[i-suspicious_string_size:i]
        keyword = self.from_suspicious_string_to_task_sentence(suspicious_string)
        return keyword

    def find_task_sentence_by_grammar(self, m_words):
        """
        メカブオブジェクトのリストにした文から、センテンスとして
        正しいところで区切ったメカブオブジェクトのリストの文を返す。
        文の最後から、名詞→格助詞のパターンを探す。
        :param m_words:
        """
        # 名詞→格助詞のパターン！
        m_result_words = self.with_pattern_from_m_words(m_words, self.index_of_noun_casemarking_particle)
        if m_result_words:
            return m_result_words

        # 名詞→動詞のパターン！
        m_result_words = self.with_pattern_from_m_words(m_words, self.index_of_noun_verb)
        if m_result_words:
            return m_result_words

        # タスクのパターンを発見できなかったorz 失敗だ。これはタスクではなさそう……。
        return None

    def with_pattern_from_m_words(self, m_words, method):
        # 名詞→格助詞のパターンが見つかったときの名詞のインデックス位置
        i = method(m_words)

        # パターンが見つかっていなかったときiはNoneになる
        if i is None:
            return None

        # パターンで見つけていたときは、名詞→格助詞の名詞から後を返す
        return m_words[i:]

    def index_of_noun_casemarking_particle(self, m_words):
        for i, m_word in enumerate(m_words):
            # 文の最後まできて見つからなかったら失敗
            if i + 1 == len(m_words):
                return None
            # まず名詞を見つける
            if m_word.type == '名詞':
                subtype = m_words[i + 1].subtype
                if subtype == '格助詞' or subtype == '連体化':
                    return i

    def index_of_noun_verb(self, m_words):
        for i, m_word in enumerate(m_words):
            # 文の最後まできて見つからなかったら失敗
            if i + 1 == len(m_words):
                return None
                # まず名詞を見つける
            if m_word.type == '名詞':
                if m_words[i + 1].type == '動詞':
                    return i

    def slice_after_dots(self, string):
        for dot in ['、', '。', '，', '〜', '～',
                    '．', '.', ',', '…', '?', '？', '!', '！']:
            if dot in string:
                # 、や。のあとの部分だけを選ぶ
                string = string.split(dot)[-1]
        return string

    def from_suspicious_string_to_task_sentence(self, suspicious_string):
        m_suspicious_words = self.prepare_task_sentence(suspicious_string)
        if m_suspicious_words is None:
            return ''
        if m_suspicious_words is []:
            return ''
        if len(m_suspicious_words) == 1:
            task_sentence = m_suspicious_words[-1].name
            return task_sentence
        m_task_words = self.find_task_sentence_by_grammar(m_suspicious_words)
        if m_task_words:
            words = [m_task_word.name for m_task_word in m_task_words]
            task_sentence = ''.join(words)
            return task_sentence
        else:
            return None

    # page.build_heading_tree() でツリーを作る。すでにself.htmlはfetchずみ
    def build_heading_tree(self):
        """
        h1
        ul>li
        h2
        h2
        の場合は、……。
        node.lisにセットする
        h1で分けた場合、トップが1つとは限らない。なのでtop_nodesとしている
        self.top_heading_nodes == root; root.heading_title = 'nanapi!!'; root.children == [node1, node2, ...]
        self.top_nodes[0].children[0].li_texts => 'まずやること', 'つぎに'
        self.top_nodes[0].children[0].children[0].heading_title => 服を洗濯する
        """
        root_node = Node(self.html_body, 'h0')
        root_node.set_descendants()
        self.top_nodes = root_node.children

    # tree = page.heading_tree()
    def heading_tree(self):
        pass

    def set_lines_from_texts(self):
        #result_page単体が実行する
        self.lines = self.text_body.split('。')

    def set_line_clusters_around_action_word(self):
        #result_page単体が実行
        self.line_clusters_around_action_word = []
        sorted_line_nums = sorted(self.line_nums_around_action_word)
        nugget_lines = []
        for i, num in enumerate(sorted_line_nums):
            nugget_lines.append(self.lines[num])
            if num is sorted_line_nums[-1]: # => 最後のそして最大の数字
                self.line_clusters_around_action_word.append(nugget_lines)
                break
            next_num = sorted_line_nums[i + 1]
            if next_num > num + 1:
                self.line_clusters_around_action_word.append(nugget_lines)
                nugget_lines = []
                continue

    def find_lines_with_action_word_from_result_page(self, action_word):
        for result_page in self.result_pages:
            # result_pageはWebPageオブジェクト
            # result_pageは1つのWebページ

            result_page.set_lines_from_texts()
            # result_page.lines => ['aa', 'bb', ...]

            result_page.set_line_nums_with_word(action_word)
            # result_page.line_nums_has_action_word => [3, 8, 12]

    def set_line_nums_around_action_word(self):
        self.line_nums_around_action_word = set([])
        for num in self.line_nums_with_action_word:
            if num == 0: #最初の行にaction_wordがあるとき
                self.line_nums_around_action_word.add(num)
                if len(self.line_nums_with_action_word) is 1:
                    # 1行だけの文章のとき
                    break
                self.line_nums_around_action_word.add(num + 1)
                continue
            elif num == len(self.lines) - 1:
                self.line_nums_around_action_word.add(num - 1)
                self.line_nums_around_action_word.add(num)
                break # linesの最後なので最後であること確定
            else:
                self.line_nums_around_action_word.add(num - 1)
                self.line_nums_around_action_word.add(num)
                self.line_nums_around_action_word.add(num + 1)

    def set_line_nums_with_word(self, word):
        #1つのwebページであるresult_pageが実行する。
        self.line_nums_with_action_word = set([])
        for index, line in enumerate(self.lines):
            if word in line:
                self.line_nums_with_action_word.add(index)

    def pick_texts_to_result_pages(self):
        self.result_pages = set([])
        text_elements = pq(self.xml_body.encode('utf-8')).find('str[name="text"]')
        for elem in text_elements:
            result_page = WebPage('unknown')
            result_page.text_body = elem.text
            self.result_pages.add(result_page)

    def find_action_word(self, action_word):
        snippet_and_title = [self.snippet, self.title]
        for text in snippet_and_title:
            start_index = text.find(action_word + 'と')
            if start_index > -1:
                possible_to_include_action_word = text[start_index + len(action_word) + 1:10]
                m_words = self.to_m_words(possible_to_include_action_word)
                if len(m_words) > 0:
                    if m_words[0].subtype == 'サ変接続':
                        self.action_word = m_words[0]


    def find_tasks_from_texts(self):
        verbs = []
        item = WebItem()
        for line in self.lines:
            mecabed_words = item.to_m_words(line)
            for m_word in mecabed_words:
                if m_word.type == '動詞':
                    verbs.append(m_word)
        return verbs

    def set_title(self):
        title = pq(self.html_body).find('title').text()
        self.title = title

    def pick_something(self):
        #多目的用途。研究には使わない。自由に書きかえて大丈夫
        text = pq(self.html).find('td>a>font').text()
        words = text.split(' ')
        normalized_words = []
        for word in words:
            word = word.lower()
            word = word.replace('_', '-')
            word = '"' + word + '",'
            normalized_words.append(word)
        return normalized_words

    def pick_key_phrases(self):
        results = pq(self.xml_body.encode('utf-8')).children()
        if not results:
            return []
        key_phrases = []
        for result in results:
            key_phrase = result[0].text
            key_phrases.append(key_phrase)
        return key_phrases

    def add_object_terms_to_dictionary(self, dictionary):
        for task in self.tasks:
            dictionary.add(task.object)

