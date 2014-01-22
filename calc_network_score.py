# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver import PickleFileSaver
from pickle_file_loader import PickleFileLoader


if __name__ == '__main__':
    query = '掃除　方法'
    pfl = PickleFileLoader()
    pages = pfl.load_fetched_pages_with_query(query)
    gtm = GraphTaskMapper()

    for page in pages[:3]:
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
