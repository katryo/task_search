# -*- coding: utf-8 -*-
import constants
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from path_mover import PathMover
from page_data_inserter import PageDataInserter
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_4
    pfl = PickleFileLoaderForOriginal()
    saver = PickleFileSaverForOriginal()
    pm = PathMover()
    di = PageDataInserter()
    for i, query in enumerate(queries):
        pages = pfl.load_fetched_pages_with_query(query)
        pm.go_or_create_and_go_to(constants.FETCHED_PAGES_O_DIR_NAME)
        pm.go_or_create_and_go_to(query)
        for i, page in enumerate(pages):
            if '.pdf' in page.url:
                continue
            if di.has_body(page.query, page.url):
                print(str(i))
                continue
            try:
                print('%i番目の%sのページをフェッチします' % (i, query))
                page.fetch_html()
                print('%sのフェッチ完了!' % page.title)
                page.set_text_from_html_body()
                #page.set_sentences_from_text()
                #filename = '%s_%i.pkl' % (query, i)
                text = page.text.replace(';', '').replace('"', '')
                di.update_body(text, page.url)
                #saver.save_file(obj=page, filename=filename)
                print('%sの保存完了!' % page.title)
                #pfs.save_pages_with_query_expansion()
            except (ValueError, IndexError, KeyboardInterrupt):
                print('%sのフェッチに失敗しました' % page.title)
                continue
        pm.go_up()
        pm.go_up()



