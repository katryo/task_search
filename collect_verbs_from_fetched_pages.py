import constants
import utils
import pickle
import pdb
import re


def set_verbs_and_sahens(page):
    page.verbs = []
    page.sahens = []
    for sentence in page.sentences:
        m_words = utils.m_words(sentence)
        for m_word in m_words:
            if m_word.type == '動詞':
                page.verbs.append(m_word.stem)
            if m_word.subtype == 'サ変接続':
                page.sahens.append(m_word.stem)


if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        set_verbs_and_sahens(page)
    for i, page in enumerate(pages):
        with open('%s_%s.pkl' % (constants.FINAL_QUERY, str(i)), 'wb') as f:
            pickle.dump(page, f)
