from pickle_file_loader import PickleFileLoader
from path_mover import PathMover
import constants
import os
import pickle
import pdb


class PickleFileLoaderForEntailmentDicts(PickleFileLoader):
    def load_object_term_dictionary(self):
        os.chdir(constants.OBJECT_TERM_DICTIONARY_DIR_NAME)
        with open(constants.OBJECT_TERM_DICTIONARY_PICKLE_FILENAME, 'rb') as f:
            object_term_dictionary = pickle.load(f)
            print('%sのロード完了!' % constants.OBJECT_TERM_DICTIONARY_PICKLE_FILENAME)
        os.chdir('..')
        return object_term_dictionary

    def load_entailment_dictionaries(self):
        os.chdir(constants.ENTAILMENT_DICTIONARIES_DIR_NAME)
        dictionaries = dict()
        for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
            for entailment_type in constants.ENTAILMENT_DICTIONARY_TYPES:
                with open('%s_%s.pkl' % (filename, entailment_type), 'rb') as f:
                    d = pickle.load(f)
                    dictionaries[filename + '_' + entailment_type] = d
        os.chdir('..')
        return dictionaries
