import utils
import constants
import pickle
import os
import pdb
from sklearn.feature_extraction.text import TfidfVectorizer


def is_bigger_than_min_tfidf(term, terms, tfidfs):
    '''
    [term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)]で使う
    list化した、語たちのtfidfの値のなかから、順番に当てる関数。
    tfidfの値がMIN_TFIDFよりも大きければTrueを返す
    '''
    if tfidfs[terms.index(term)] > constants.MIN_TFIDF:
        return True
    return False


def tfidf_sahen_or_verb(pages):
    # analyzerは文字列を入れると文字列のlistが返る関数
    vectorizer = TfidfVectorizer(analyzer=utils.sahens_or_verbs, min_df=1, max_df=50)
    corpus = [page.text for page in pages]
    x = vectorizer.fit_transform(corpus)
    return x, vectorizer  # xはtfidf_resultとしてmainで受け取る


def tfidf_stem(pages):
    # analyzerは文字列を入れると文字列のlistが返る関数
    vectorizer = TfidfVectorizer(analyzer=utils.stems, min_df=1, max_df=50)
    corpus = [page.text for page in pages]
    x = vectorizer.fit_transform(corpus)
    return x, vectorizer  # xはtfidf_resultとしてmainで受け取る

def is_bigger_than_min_tfidf(term, terms, tfidfs):
    '''
    [term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)]で使う
    list化した、語たちのtfidfの値のなかから、順番に当てる関数。
    tfidfの値がMIN_TFIDFよりも大きければTrueを返す
    '''
    if tfidfs[terms.index(term)] > constants.MIN_TFIDF:
        return True
    return False

if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()  # pagesはhtmlをフェッチしてtextにセットずみ
    tfidf_result, vectorizer = tfidf_sahen_or_verb(pages)  # tfidf_resultはtfidf関数のx

    pkl_tfidf_result_path = os.path.join('..', constants.TFIDF_RESULT_PKL_FILENAME)
    pkl_tfidf_vectorizer_path = os.path.join('..', constants.TFIDF_VECTORIZER_PKL_FILENAME)

    with open(pkl_tfidf_result_path, 'wb') as f:
        pickle.dump(tfidf_result, f)
    with open(pkl_tfidf_vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)

    terms = vectorizer.get_feature_names()
    for i in range(constants.NUM_OF_FETCHED_PAGES * len(constants.QUERIES)):
        tfidfs = tfidf_result.toarray()[i]
        print([term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)])
    pdb.set_trace()