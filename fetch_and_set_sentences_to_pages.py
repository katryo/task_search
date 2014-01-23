# -*- coding: utf-8 -*-
import constants
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver
from sentence_separator import SentenceSeparator

if __name__ == '__main__':
    query = '部屋　掃除する'
    pfs = PickleFileLoader()
    pages = pfs.load_fetched_pages_with_query(query)
    sp = SentenceSeparator()
    for page in pages:
        try:
            page.fetch_html()
            print('%sのフェッチ完了!' % page.title)
            page.set_text_from_html_body()
            page.set_sentences_from_text()
            pfs.save_pages_with_query_expansion()
        except (ValueError, IndexError):
            continue

    saver = PickleFileSaver()
    saver.save_pages_with_dir_name(pages, constants.QUERY)

