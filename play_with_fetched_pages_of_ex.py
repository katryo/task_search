# -*- coding: utf-8 -*-
import pdb
import constants
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    loader = PickleFileLoader()
    pages = loader.load_fetched_pages_with_query_and_expansion_word('春　楽しむ', '')
    pdb.set_trace()