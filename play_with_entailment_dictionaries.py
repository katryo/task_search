# -*- coding: utf-8 -*-
import utils
import pdb
import constants

if __name__ == '__main__':
    dictionaries = utils.load_entailment_dictionaries()
    pages = utils.load_fetched_pages()
    for dictionary_type in constants.ENTAILMENT_DICTIONARY_TYPES:
        for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
            for page in pages:
                for task in page.tasks:
                    if task.predicate_term in dictionaries[filename + '_' + dictionary_type]:
                        for term in dictionaries[filename + '_' + dictionary_type][task.predicate_term]:
                            print('%s %s %s changes into %s %s %s %s' %
                                  (
                                      task.object_term.name,
                                      task.cmp,
                                      task.predicate_term,
                                      task.object_term.name,
                                      term,
                                      task.cmp,
                                      filename
                                  ))