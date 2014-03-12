# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
import constants


if __name__ == '__main__':
    original_queries = constants.QUERIES_4
    pfs = PickleFileSaverForOriginal()
    pfl = PickleFileLoaderForOriginal()
    for query in original_queries:
        print(query)
        pages = pfl.load_fetched_pages_with_query(query)
        counter = 0
        for page in pages:
            if page.tasks:
                print(counter)
                counter += 1
        print('added all edges!')
