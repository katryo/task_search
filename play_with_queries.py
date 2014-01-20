# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    pfl = PickleFileLoader()
    queries = pfl.load_queries()
    pdb.set_trace()