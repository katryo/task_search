# -*- coding: utf-8 -*-
import pdb
import constants
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    loader = PickleFileLoader()
    pages = loader.load_fetched_pages_with_query(constants.QUERY)
    pdb.set_trace()