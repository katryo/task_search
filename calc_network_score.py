# -*- coding: utf-8 -*-
import networkx as nx
import pdb
import utils
from sqlite_data_loader import SQLiteDataLoader
import constants


if __name__ == '__main__':
    g = nx.DiGraph()
    pages = utils.load_fetched_pages()
    sqldl = SQLiteDataLoader()
    entailment_dictionaries = utils.load_entailment_dictionaries()

    for page in pages[:20]:
        for task in page.tasks:
            # まずオリジナルのノードを追加
            g.add_node('%s_%s' % (task.object_term.name, task.predicate_term))
            # print('%s_%s' % (task.object_term.name, task.predicate_term))

            # object_term.core_nounのhypohypeを探す
            hypes = sqldl.select_hypes_with_hypo(task.object_term.name)
            # hypos = sqldl.select_hypos_with_hype(task.object_term.name)

            entailing_predicates = []
            for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
                if task.predicate_term in entailment_dictionaries[filename + '_entailing']:
                    entailings = entailment_dictionaries[filename + '_entailing'][task.predicate_term]
                    entailing_predicates.extend(list(entailings))

            entailed_predicates = []
            for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
                if task.predicate_term in entailment_dictionaries[filename + '_entailed']:
                    entaileds = entailment_dictionaries[filename + '_entailed'][task.predicate_term]
                    entailed_predicates.extend(list(entaileds))

            # 4種類の上位語・下位語が揃った。
            for hype_or_hype_or_original in (hypes + [task.object_term.name]):
                for entailing_or_entailed_or_original in (entailing_predicates
                                                          + entailed_predicates + [task.predicate_term]):
                    if hype_or_hype_or_original == '収録曲':
                        continue
                    g.add_node('%s_%s' % (hype_or_hype_or_original, entailing_or_entailed_or_original))
                    # オリジナルのノードから、上位・下位に貼る。自分自身にも貼っている。
                    g.add_edge('%s_%s' %
                               (task.object_term.name, task.predicate_term),
                               '%s_%s' %
                               (hype_or_hype_or_original, entailing_or_entailed_or_original))
    print('added all edges!')
    results = g.in_degree()
    print([(result + str(results[result])) for result in results if results[result] > 1])

'''
    results = nx.pagerank(g)
    for result in results:
        #print(result + str(results[result]))
        if results[result] > 9.6e-06:
            print(result + str(results[result]))
            '''
    # print([(result + str(results[result]) for result in results if results[result] > 0.1)])
    # 1エッジで4.1秒
    # 1ノードにつき10エッジで16秒
    # 20エッジで32秒。線形ぽい。
    # おそらく200エッジで300秒ほど。つまり5分。
    # 1000エッジで1500秒 = 25分。まあいけそう。いざとなったらEC2借りよう。

