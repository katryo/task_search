# -*- coding: utf-8 -*-
import constants
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver
from path_mover import PathMover
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES
    pfl = PickleFileLoader()
    saver = PickleFileSaver()
    pm = PathMover()
    for query in queries:
        pages = pfl.load_fetched_pages_with_original_query(query)
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_O_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        for i, page in enumerate(pages):
            if hasattr(page, 'sentences'):
                if page.sentences:
                    print('%sはもうsentencesがあります' % page.title)
                    continue
            try:
                page.fetch_html()
                print('%sのフェッチ完了!' % page.title)
                page.set_text_from_html_body()
                page.set_sentences_from_text()
                filename = '%s_%i.pkl' % (query, i)
                saver.save_file(obj=page, filename=filename)
                print('%sの保存完了!' % page.title)
                #pfs.save_pages_with_query_expansion()
            except (ValueError, IndexError):
                print('%sのフェッチに失敗しました' % page.title)
                continue
        pm.go_up()
        pm.go_up()



