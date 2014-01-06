# -*- coding: utf-8 -*-
import constants
import pdb
from toiu_searcher import ToiuSearcher
from pickle_file_loader import PickleFileLoader
from m_words_factory import MWordsFactory

STOP_WORDS = ['名前', 'もの', '概念', 'こと']

if __name__ == '__main__':
    pfl = PickleFileLoader()
    results_dic = pfl.load_simple_task_search_result()
    results_set = set()
    for result_broader in results_dic:
        results_set.add(results_dic[result_broader])

    ts = ToiuSearcher()
    concrete_terms = dict()
    pdb.set_trace()
    for simple_result in results_set:
        concrete_object_terms = set()  # 1つのsimple_resultにつき複数のconcrete_otがある
        object_term, predicate_term = simple_result.split('_')
        result_pages = ts.result_pages(object_term, constants.FINAL_QUERY)
        for page in result_pages:
            # snippetの括弧を除去して、（）内を除去して、メカブして、
            # 「というobject_term」の直前が名詞だったとき、それを答えとする
            snippet = page.snippet_without_parenthesis()
            m_words_factory = MWordsFactory()
            m_words_of_snippet = m_words_factory.build_from(snippet)
            for i, m_word in enumerate(m_words_of_snippet):
                if m_word.name == object_term:
                    if m_words_of_snippet[i-1].word_info == 'という  助詞,格助詞,連語,*,*,*,という,トイウ,トユウ':
                        if m_words_of_snippet[i-2].type == '名詞':
                            if m_words_of_snippet[i-2].name in STOP_WORDS:
                                continue
                            concrete_object_terms.add(m_words_of_snippet[i-2].name + '_' + predicate_term)
        concrete_terms[simple_result] = concrete_object_terms
    print(concrete_terms)