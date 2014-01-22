# -*- coding: utf-8 -*-
import pdb
import constants
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver import PickleFileSaver
from pickle_file_loader import PickleFileLoader


if __name__ == '__main__':
    pfl = PickleFileLoader()
    pages = pfl.load_fetched_pages_with_query(constants.QUERY)
    gtm = GraphTaskMapper()

    for page in pages:
        for task in page.tasks:
            # ここでpart_of関係に繋がるorder=1のエッジを与えたい
            # ノードに与える？ エッジに与える？
            # 選択肢1: ノードにurlを与えてorderも与える。part-ofを数えるときは、order1以上のノードを数えて、それと同じurlのものをエッジで繋ぐ。

            # 選択肢2:すべてエッジで表現。
            # 結論；エッジはめんどう。ノードにattr与えよう。
            gtm.add_node_and_edge_with_task(task)
        print('Tasks on %s are added!' % page.title)
    print('added all edges!')
    results_dic = gtm.broader_nodes_with_higher_in_degree_score()
    pfs = PickleFileSaver()
    pfs.save_simple_task_search_result_with_query(results_dic, constants.QUERY)