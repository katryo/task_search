# -*- coding: utf-8 -*-
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_saver_for_ex import PickleFileSaverForEx
from path_mover import PathMover
import constants
import pdb
import os


if __name__ == '__main__':
    pfl = PickleFileLoaderForExpandedQuery()
    pfs = PickleFileSaverForEx()
    pm = PathMover()

    original_queries = constants.QUERIES_1

    pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
    for original_query in original_queries:
        pm.go_or_create_and_go_to(original_query)
        expanded_queries = os.listdir()
        for expanded_query in expanded_queries:
            if expanded_query == '.DS_Store' or expanded_query == 'tasks.sqlite':
                continue
            pm.go_or_create_and_go_to(expanded_query)
            filenames = os.listdir()
            print('拡張クエリは%sです' % expanded_query)
            for i, filename in enumerate(filenames):
                print('ファイル名は%sです' % filename)
                if filename == '.DS_Store' or expanded_query == 'tasks.sqlite':
                    continue
                try:
                    page = pfl.load_file(filename)
                except EOFError:
                    print('%sのファイルをロードできません！' % expanded_query)
                    break
                if hasattr(page, 'tasks'):
                    if page.tasks:
                        print('すでにtasksがあります')
                        # continue
                page.set_tasks_from_sentences()
                print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))
                pfs.save_file(obj=page, filename=filename)
                print('%sの保存完了!' % page.title)
            pm.go_up()
        pm.go_up()
    pm.go_up()

