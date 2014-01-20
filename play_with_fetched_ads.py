# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader import PickleFileLoader
from term_counter import TermCounter

if __name__ == '__main__':
    loader = PickleFileLoader()
    ads = loader.load_ads_with_query('クレー射撃　体験')
    sahens = []
    for ad in ads:
        ad.set_sahens_from_title_and_snippet()
        sahens.extend(ad.sahens)
    counter = TermCounter()
    counter.count_terms(sahens)
    print(counter.term_count)
    pdb.set_trace()
