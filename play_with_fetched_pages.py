# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader_for_original import PickleFileLoaderForOriginal

if __name__ == '__main__':
    loader = PickleFileLoaderForOriginal()
    pages = loader.load_fetched_pages_with_query('花粉症　を　対策する')
    task_set = set()
    for page in pages:
        tasks = page.tasks
        for task in tasks:
            task_set.add(task)
    print(len(task_set))
