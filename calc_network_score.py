# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver import PickleFileSaver
from pickle_file_loader import PickleFileLoader


if __name__ == '__main__':
    query = '掃除　方法'
    pfl = PickleFileLoader()
    g = pfl.load_graph_with_query(query)
    for node in g.nodes():
        edges = g[node]
        for generalized_task in edges:
            entailment_type = edges[generalized_task].get('entailment_type')
            if entailment_type == 'nonent_predi' or entailment_type == 'ent_presu':
                aspects = g.node[generalized_task]['aspects']
                for aspect in aspects:
                    #ひとつでもis_originalであれば次に進める
                    if g.node[generalized_task]['aspects']['is_original']:
                        print('%s is a part-of %s because of entailment' % (node, generalized_task))
                        continue
                print('%s is a part-of %s, but the later is not a original task' % (node, generalized_task))
                # 次はorderでpart-ofを発見
                # 貢献度があり、同じurlで、
                # 汎化は1.頻度を調べて、2.part-of3subtype-ofを調べている。
                # urlが同じであればそれはある上位タスク（おそらくクエリ）のpart-ofであることを意味する

            is_hype = edges[generalized_task].get('is_hype')
            if is_hype:
                if g.node[generalized_task]['is_original']:
                    print('%s is a subtype-of %s' % (node, generalized_task))
                    continue
                print('%s is a subtype-of %s, but the later is not a original task' % (node, generalized_task))

    pdb.set_trace()
    pages = pfl.load_fetched_pages_with_query(query)
    gtm = GraphTaskMapper()

    for page in pages[2:3]:
        for task in page.tasks:
            # ここでpart_of関係に繋がるorder=1のエッジを与えたい
            # ノードに与える？ エッジに与える？
            # 選択肢1: ノードにurlを与えてorderも与える。part-ofを数えるときは、order1以上のノードを数えて、それと同じurlのものをエッジで繋ぐ。

            # 選択肢2:すべてエッジで表現。
            # 結論；エッジはめんどう。ノードにattr与えよう。
            gtm.add_node_and_edge_with_task(task)
        print('Tasks on %s are added!' % page.title)
    print('added all edges!')
    pfs = PickleFileSaver()
    pfs.save_graph_with_query(obj=gtm.graph, query=query)
    results_dic = gtm.frequent_tasks_by_generalized_tasks()
    print(results_dic)
    pdb.set_trace()
