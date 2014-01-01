# -*- coding: utf-8 -*-
import utils
import constants
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    # pdb.set_trace()
    for i, page in enumerate(pages):
        tasks = page.obj_and_predicate_dict_by_wo_from_sentences()
        if tasks:
            for task in tasks:
                object = task.object
                predicate = task.predicate
                cmp = task.cmp
                dictionaries = utils.load_entailment_dictionaries()
                for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
                    if predicate in dictionaries[filename].keys():
                        a = dictionaries[filename][predicate]
                        print('%s %s %s entails %s %s %s %s %s' % (object, cmp, predicate, object, cmp, a, filename, page.url))
            # print('%i番目のWebPage' % i)
