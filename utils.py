import constants
import os
import pickle
import MeCab
from mecabed_word import MecabedWord


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
