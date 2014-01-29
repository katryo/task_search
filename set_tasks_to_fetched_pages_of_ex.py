# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver
from path_mover import PathMover
import constants
import pdb
import os

if __name__ == '__main__':
    pfl = PickleFileLoader()
    pfs = PickleFileSaver()
    pm = PathMover()

    original_queries = ['小学校　受験させる']

    pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
    for original_query in original_queries:
        pm.go_or_create_and_go_to(original_query)
        expanded_queries = os.listdir()
        for expanded_query in expanded_queries:
            if 'graph' in expanded_query:
                continue
            if expanded_query == '.DS_Store':
                continue
            pm.go_or_create_and_go_to(expanded_query)
            filenames = os.listdir()
            for i, filename in enumerate(filenames):
                if filename == '.DS_Store':
                    continue
                page = pfl.load_file(filename)
                if hasattr(page, 'tasks'):
                    if page.tasks:
                        print('すでにtasksがあります')
                        continue
                page.set_tasks_from_sentences()
                print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))
                pfs.save_file(obj=page, filename=filename)
                print('%sの保存完了!' % page.title)
            pm.go_up()
        pm.go_up()
    pm.go_up()

