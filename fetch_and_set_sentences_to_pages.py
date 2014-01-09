# -*- coding: utf-8 -*-
import constants
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver
from sentence_separator import SentenceSeparator

if __name__ == '__main__':
    loader = PickleFileLoader()
    pages = loader.load_fetched_pages()
    sp = SentenceSeparator()
    for page in pages:
        try:
            page.fetch_html()
            print('%sのフェッチ完了!' % page.title)
            page.set_text_from_html_body()
            page.sentences = sp.split_by_dots(page.text)
        except (ValueError, IndexError):
            continue

    saver = PickleFileSaver()
    saver.save_pages_with_dir_name(pages, constants.QUERY)

