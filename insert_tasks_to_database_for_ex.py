# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery
import constants


if __name__ == '__main__':
    original_queries = constants.QUERIES_1
    pfl = PickleFileLoaderForExpandedQuery()
    for query in original_queries:
        pages = pfl.load_fetched_pages_with_query(query)

        for i, page in enumerate(pages):
            try:
                for task in page.tasks:
                    task.insert_task_to_database()
                print('%i 番目のページ %s のタスクをDBに入れました' % (i, page.title))
            except AttributeError:
                break
        print('%sのぶんはおしまい！' % query)
