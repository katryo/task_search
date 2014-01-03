# -*- coding: utf-8 -*-
import utils
import constants
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    for page in pages:
        for task in page.tasks:
            print('%s, %s' % (task.object_term.name, task.object_term.context))
    """
    for i, page in enumerate(pages):
        tasks = page.obj_and_predicate_dict_by_wo_from_sentences()
        if tasks:
            for task in tasks:
                object = task.object
                predicate = task.predicate
                cmp = task.cmp
                dictionaries = utils.load_entailment_dictionaries()
                for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
                    # まってまって。1辞書にも複数のentails可能性があるよ！
                    if predicate in dictionaries[filename].keys():
                        a = dictionaries[filename][predicate]
                        print('%s %s %s entails %s %s %s %s %s' % (object, cmp, predicate, object, cmp, a, filename, page.url))
            # print('%i番目のWebPage' % i)

"""