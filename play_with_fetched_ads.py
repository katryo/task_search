# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader_for_ads import PickleFileLoaderForAds
from term_counter import TermCounter

if __name__ == '__main__':
    loader = PickleFileLoaderForAds()
    ads = loader.load_ads_with_query('花粉症　対策する')
    sahens = []
    for ad in ads:
        ad.set_sahens_from_title_and_snippet()
        sahens.extend(ad.sahens)
    counter = TermCounter()
    counter.count_terms(sahens)
    print(counter.term_count)
