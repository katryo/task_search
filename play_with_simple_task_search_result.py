# -*- coding: utf-8 -*-
import pdb
import constants
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    pfl = PickleFileLoader()
    results_dic = pfl.load_simple_task_search_result_with_query(constants.QUERY)
    results_set = set()
    for broader_word in results_dic:
        narrower_tasks = results_dic[broader_word]
        for task in narrower_tasks:
            results_set.add(task)
    print(results_set)
    pdb.set_trace()