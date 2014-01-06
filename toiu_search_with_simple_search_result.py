# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader import PickleFileLoader
from object_predicate_toiu_searcher import ObjectPredicateToiuSearcher

if __name__ == '__main__':
    pfl = PickleFileLoader()
    results_dic = pfl.load_simple_task_search_result()
    ops = ObjectPredicateToiuSearcher()
    concrete_terms = ops.concrete_terms(results_dic)
    print(concrete_terms)