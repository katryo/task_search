# -*- coding: utf-8 -*-
import pdb
import constants
from pickle_file_loader import PickleFileLoader

if __name__ == '__main__':
    pfl = PickleFileLoader()
    dictionaries = pfl.load_entailment_dictionaries()
    pages = pfl.load_fetched_pages_with_query(constants.QUERY)
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