# -*- coding: utf-8 -*-
from pickle_file_loader import PickleFileLoader
from pickle_file_saver import PickleFileSaver

if __name__ == '__main__':
    query = '掃除　方法'
    pfl = PickleFileLoader()
    pages = pfl.load_fetched_pages_with_query(query)
    for i, page in enumerate(pages):
        page.set_tasks_from_sentences()
        print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))

    pfs = PickleFileSaver()
    pfs.save_pages_with_query(pages, query)
