# -*- coding: utf-8 -*-
import pdb
import constants
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    loader = PickleFileLoader()
    ads = loader.load_ads_with_query('クレー射撃　体験')
    for ad in ads:
        ad.snippet
    pdb.set_trace()
