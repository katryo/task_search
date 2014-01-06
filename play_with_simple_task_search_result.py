# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    pfl = PickleFileLoader()
    results_dic = pfl.load_simple_task_search_result()
    pdb.set_trace()