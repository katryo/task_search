import constants
import os
import pickle
import MeCab
from mecabed_word import MecabedWord
from itertools import chain
from web_page import WebPage
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

def load_all_fetched_pages():
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
    pages = []
    for query in constants.QUERIES:
        os.chdir(query)
        for i in range(constants.NUM_OF_FETCHED_PAGES):
            with open('%s_%s.pkl' % (query, str(i)), 'rb') as f:
                page = pickle.load(f)
                page.set_text_from_html_body()
                pages.append(page)
        os.chdir('..')
    os.chdir('..')  # トップディレクトリに戻る
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

def sahens_or_verbs(text):
    s_list = sahens(text)
    v_list = verbs(text)
    return s_list + v_list

def sahens(string):
    keywords = []
    mwords = m_words(string)
    for m_word in mwords:
        if m_word.subtype == 'サ変接続':
            item = m_word.name
            keywords.append(item)
    return keywords

def verbs(text):
    keywords = []
    mwords = m_words(text)
    for m_word in mwords:
        if m_word.type == '動詞':
            item = m_word.stem
            keywords.append(item)
    return keywords


def _split_to_words(text, to_stem=False):
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


def words(text):
    words = _split_to_words(text, to_stem=False)
    return words


def stems(text):
    stems = _split_to_words(text, to_stem=True)
    return stems


def load_all_html_files():
    pages = []
    for query in constants.QUERIES:
        os.chdir(query)
        pages.extend(load_html_files_with_query(query))
        os.chdir('..')
    return pages


def load_html_files_with_query(query):
    pages = []
    for i in range(constants.NUM_OF_FETCHED_PAGES):
        with open('%s_%s.html' % (query, str(i)), 'r') as f:
            page = WebPage()
            page.html_body = f.read()
        page.remove_html_tags()
        pages.append(page)
    return pages

def load_html_files():
    """
    HTMLファイルがあるディレクトリにいる前提で使う
    """
    pages = load_html_files_with_query(constants.FINAL_QUERY)
    return pages


def go_to_fetched_pages_dir():
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)


def save_all_pages(pages):
    # fetched_pagesのひとつ上のディレクトリからfetched_pagesに降りる
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
    for query in constants.QUERIES:
        os.chdir(query)
        for i in range(constants.NUM_OF_FETCHED_PAGES):
            num_of_page = constants.QUERIES.index(query) * 50 + i
            with open('%s_%i.pkl' % (query, i), 'wb') as f:
                pickle.dump(pages[num_of_page], f)
                print('%s_%i.pklの保存完了!' % (query, i))
        os.chdir('..')


def target_from_m_words_and_wo_i(m_words, wo_i):
    targets = m_words[:wo_i]
    for m_word in reversed(targets):
        if m_word.type == '名詞':
            return m_word.name
    return '?'


def action_from_m_words_and_wo_i(m_words, wo_i):
    action_like_m_words = m_words[wo_i:]
    for i, m_word in enumerate(action_like_m_words):
        if m_word.type == '動詞':
            if 'サ変接続' in action_like_m_words[i-1].word_info:
                return action_like_m_words[i-1].stem
            return m_word.stem
    return '?'