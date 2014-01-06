# -*- coding: utf-8 -*-
import constants
from toiu_searcher import ToiuSearcher
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    pfl = PickleFileLoader()
    results_dic = pfl.load_simple_task_search_result()
    results_set = ()
    for result_broader in results_dic:
        results_set.add(results_dic[result_broader])

    ts = ToiuSearcher()
    for simple_result in results_set:
        object_term, predicate_term = simple_result.split('_')
        result_pages = ts.result_pages(object_term, constants.FINAL_QUERY)
        for page in result_pages:
            # snippetの括弧を除去して、（）内を除去して、メカブして、
            # 「というobject_term」の直前が名詞だったとき、それを答えとする