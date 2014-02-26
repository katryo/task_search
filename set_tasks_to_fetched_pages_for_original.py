# -*- coding: utf-8 -*-
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from page_data_loader import PageDataLoader
import constants
from sentence import Sentence
import pdb

if __name__ == '__main__':
    queries = constants.QUERIES_4
    for query in queries:
        pfl = PickleFileLoaderForOriginal()
        pages = pfl.load_fetched_pages_with_query(query)
        for i, page in enumerate(pages):
            with PageDataLoader() as page_loader:
                sentences = page_loader.sentences_with_id(page.id)
                page.sentences = []
                for sentence in sentences:
                    page.sentences.append(Sentence(sentence, page.query))
            page.set_tasks_from_sentences()
            print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))

        pfs = PickleFileSaverForOriginal()
        pfs.save_pages_with_query(pages=pages, query=query)
