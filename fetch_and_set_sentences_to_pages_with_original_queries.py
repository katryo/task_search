# -*- coding: utf-8 -*-
import constants
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from path_mover import PathMover
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_4
    #queries = ['保育園　入園させる']
    pfl = PickleFileLoaderForOriginal()
    saver = PickleFileSaverForOriginal()
    pm = PathMover()
    for i, query in enumerate(queries):
        pages = pfl.load_fetched_pages_with_query(query)
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_O_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        for i, page in enumerate(pages):
            if hasattr(page, 'sentences'):
                if page.sentences:
                    print('%sはもうsentencesがあります' % page.title)
                    continue
            try:
                print('%i番目の%sのページをフェッチします' % (i, query))
                page.fetch_html()
                print('%sのフェッチ完了!' % page.title)
                page.set_text_from_html_body()
                page.set_sentences_from_text()
                filename = '%s_%i.pkl' % (query, i)
                saver.save_file(obj=page, filename=filename)
                print('%sの保存完了!' % page.title)
                #pfs.save_pages_with_query_expansion()
            except (ValueError, IndexError, KeyboardInterrupt):
                print('%sのフェッチに失敗しました' % page.title)
                continue
        pm.go_up()
        pm.go_up()



