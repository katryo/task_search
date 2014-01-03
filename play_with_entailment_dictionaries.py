# -*- coding: utf-8 -*-
import utils
import pdb
import constants

if __name__ == '__main__':
    dictionaries = utils.load_entailment_dictionaries()
    pdb.set_trace()
    for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
        print(dictionaries[filename])
