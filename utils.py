import constants
import os
import pickle
import MeCab
from mecabed_word import MecabedWord
from itertools import chain
import pdb


def flatten(items_in_list):

    """

    :param items_in_list: ['あいう', ['えお', 'かき'], 'くけこ']
    """
    return chain.from_iterable(items_in_list)


def split_by_dots(text):
    """
    再帰的にsplitして1つのlistにする
    """
    texts = split_texts_by_dots([text])
    # dotで繰り返しているのが話をややこしくしている。
    return texts


def split_texts_by_dots(texts):
    for dot in constants.DOTS:
        # 問題は、strとlistの型の違い
        # split_by_dotsはstrで入ってlistを返すのでそのまま再帰で使えない
        # listで入ってlistを返す関数があればいい
        # ['a。aaaa', 'bbb。bbbb', 'cccc.cc!cc']など、ひとまず'。'でsplitする
        texts = split_and_flatten_by_a_certain_dot(texts, dot)
    return texts


def visit_query_dir():
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
    if not os.path.exists(constants.FINAL_QUERY):
        os.mkdir(constants.FINAL_QUERY)
    os.chdir(constants.FINAL_QUERY)

def split_and_flatten_by_a_certain_dot(texts, dot):
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


def load_fetched_pages():
    path = os.path.join(constants.FETCHED_PAGES_DIR_NAME, constants.FINAL_QUERY)
    os.chdir(path)
    pages = []
    for i in range(constants.NUM_OF_FETCHED_PAGES):
        with open('%s_%s.pkl' % (constants.FINAL_QUERY, str(i)), 'rb') as f:
            page = pickle.load(f)
            pages.append(page)
    return pages


def m_words(str):
    tagger = MeCab.Tagger('mecabrc')
    result = tagger.parse(str)
    word_info_collection = result.split('\n')
    m_words = []
    for info in word_info_collection:
        #infoが',\t名詞,サ変接続,*,*,*,*,*'のようなときはbreakする
        if info == 'EOS' or info == '':
            break
        else:
            invalid = is_including_invalid_word(info)
            if invalid is True:
                break
            else:
                mw = MecabedWord(info)
                #mw.name => '希望'
                #mw.type => '名詞'
                #mw.subtype => 'サ変接続'
                m_words.append(mw)
    return m_words


def is_including_invalid_word(info):
    head = info[0:4]
    invalid = False
    invalid_words = [
        ',', '.', '…', '(', ')', '-',
        '/', ':', ';', '&', '%', '％',
        '~', '〜', '≪', '≫', '[', ']',
        '|', '"'
    ]
    for invalid_word in invalid_words:
        if invalid_word in head:
            invalid = True
            break
    return invalid
