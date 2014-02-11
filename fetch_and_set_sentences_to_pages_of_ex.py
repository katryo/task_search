# -*- coding: utf-8 -*-
import constants
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
from pickle_file_saver_for_ex import PickleFileSaverForEx
from path_mover import PathMover
import pdb
import os
import constants

if __name__ == '__main__':
    pfl = PickleFileLoaderForExpandedQuery()
    pfs = PickleFileSaverForEx()
    pm = PathMover()

    original_queries = constants.QUERIES_4

    pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
    for original_query in original_queries:
        pm.go_or_create_and_go_to(original_query)
        expanded_queries = os.listdir()
        for expanded_query in expanded_queries:
            if 'graph' in expanded_query:
                print('graph!')
                continue
            if expanded_query == '.DS_Store':
                continue
            pm.go_or_create_and_go_to(expanded_query)
            filenames = os.listdir()
            for i, filename in enumerate(filenames):
                if filename == '.DS_Store':
                    continue
                try:
                    page = pfl.load_file(filename)
                except EOFError:
                    print('%sのロードに失敗！' % page.title)
                    page.text = ''
                    page.sentences = ['']
                    continue
                if hasattr(page, 'text'):
                    print('%sはすでにフェッチしています' % page.title)
                    continue
                try:
                    if page.sentences:
                        continue
                    page.fetch_html()
                    page.set_text_from_html_body()
                    page.set_sentences_from_text()
                    pfs.save_file(obj=page, filename=filename)
                    print('%i番目のページ、%sの保存完了!' % (i, page.title))
                except:
                    print('%sの処理に失敗！' % page.title)
                    continue
            pm.go_up()
        pm.go_up()
    pm.go_up()

