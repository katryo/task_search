# -*- coding: utf-8 -*-
import constants
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver
from sentence_separator import SentenceSeparator
from path_mover import PathMover
import os

if __name__ == '__main__':
    pfl = PickleFileLoader()
    pfs = PickleFileSaver()
    sp = SentenceSeparator()
    pm = PathMover()

    original_queries = ['部屋　掃除する']

    pm.go_or_create_and_go_to(constants.FETCHED_PAGES_DIR_NAME)
    for original_query in original_queries:
        pm.go_or_create_and_go_to(original_query)
        expanded_queries = os.listdir()
        for expanded_query in expanded_queries:
            if expanded_query == '.DS_Store':
                continue
            pm.go_or_create_and_go_to(expanded_query)
            filenames = os.listdir()
            for i, filename in enumerate(filenames):
                if i == 100:
                    break
                if filename == '.DS_Store':
                    continue
                page = pfl.load_file(filename)
                if hasattr(page, 'text'):
                    continue
                try:
                    page.fetch_html()
                    print('%sのフェッチ完了!' % page.title)
                    page.set_text_from_html_body()
                    page.set_sentences_from_text()
                    pfs.save_file(obj=page, filename=filename)
                    print('%sの保存完了!' % page.title)
                except:
                    print('%sの処理に失敗！' % page.title)
                    continue
            pm.go_up()
        pm.go_up()
    pm.go_up()

