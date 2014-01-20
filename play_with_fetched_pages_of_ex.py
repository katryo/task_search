# -*- coding: utf-8 -*-
import pdb
import constants
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    loader = PickleFileLoader()
    pages = loader.load_fetched_pages_with_query(constants.QUERY)
    task_size = 0
    for page in pages:
        for task in page.tasks:
            task_size += 1
    print(task_size)
    pdb.set_trace()