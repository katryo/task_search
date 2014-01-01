# -*- coding: utf-8 -*-
import utils
import constants
import patterns
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    # pdb.set_trace()
    for i, page in enumerate(pages):
        results = page.obj_and_predicate_dict_by_wo_from_sentences()
        if results:
            for result in results:
                object = result['object']
                verb = result['verb']
                cmp = result['cmp']
                dictionaries = utils.load_entailment_dictionaries()
                for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
                    if verb in dictionaries[filename].keys():
                        a = dictionaries[filename][verb]
                        print('%s %s %s entails %s %s %s %s %s' % (object, cmp, verb, object, cmp, a, filename, page.url))
            # print('%i番目のWebPage' % i)
