from pickle_file_loader_for_ads import PickleFileLoaderForAds
from pickle_file_saver_for_ads import PickleFileSaverForAds
from term_counter import TermCounter
import constants
from query import Query
import pdb

if __name__ == '__main__':
    pfl = PickleFileLoaderForAds()
    for query in constants.QUERIES_4:
        adding_terms = []
        ads = pfl.load_ads_with_query(query)
        sahens = []
        for ad in ads:
            ad.set_sahens_from_title_and_snippet()
            sahens.extend(ad.sahens)
        counter = TermCounter()
        counter.count_terms(sahens)
        frequent_terms = counter.frequent_terms()
        for term in frequent_terms:
            if term in query:
                continue
            adding_terms.append(term)

        q = Query(query)
        q.set_expansion_words(adding_terms)
        pfs = PickleFileSaverForAds()
        pfs.save_query(q)
