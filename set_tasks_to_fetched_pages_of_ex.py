# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver
import constants

if __name__ == '__main__':
    for query in constants.QUERIES:
        pfl = PickleFileLoader()
        pages = pfl.load_fetched_pages_of_ex_with_query(query)
        for i, page in enumerate(pages):
            page.set_tasks_from_sentences()
            print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))
        pages_dict = {query: pages}

        pfs = PickleFileSaver()
        pfs.save_pages_with_query_expansion(pages_dict=pages_dict, original_query=query)
