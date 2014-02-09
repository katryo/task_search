# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader_for_ex import PickleFileLoaderForExpandedQuery

if __name__ == '__main__':
    loader = PickleFileLoaderForExpandedQuery()
    pages = loader.load_pages_with_task_with_query('部屋　掃除する')
    subtype_nouns = {}
    for page in pages:
        for subtype in page.subtypes:
            if not subtype in  subtype_nouns:
                subtype_nouns[subtype] = {'pages': [page]}
            subtype_nouns[subtype]['pages'].append(page)

    for subtype in subtype_nouns:
        for page in subtype_nouns[subtype]['pages']:
            if not 'tasks' in subtype_nouns[subtype]:
                subtype_nouns[subtype]['tasks'] = page.tasks
            subtype_nouns[subtype]['tasks'].extend(page.tasks)

    for subtype_noun in subtype_nouns:
        print('=======')
        print(subtype_noun)
        tasks = subtype_nouns[subtype_noun]['tasks']
        for task in tasks:
            task_string = '%s%s%s' % (task.object_term.core_noun,
                                      task.cmp,
                                      task.predicate_term)
            #print(task_string)
        print('=======')

