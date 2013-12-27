import pickle
import os
import constants
import pdb

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
    pkl_tfidf_result_path = os.path.join(constants.TFIDF_RESULT_PKL_FILENAME)
    pkl_tfidf_vectorizer_path = os.path.join(constants.TFIDF_VECTORIZER_PKL_FILENAME)
    with open(pkl_tfidf_result_path, 'rb') as f:
        tfidf_result = pickle.load(f)
    with open(pkl_tfidf_vectorizer_path, 'rb') as f:
        vectorizer =pickle.load(f)

    terms = vectorizer.get_feature_names()
    for i in range(constants.NUM_OF_FETCHED_PAGES * len(constants.QUERIES)):
        tfidfs = tfidf_result.toarray()[i]
        print([term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)])
    pdb.set_trace()
