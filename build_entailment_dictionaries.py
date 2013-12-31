# -*- coding: utf-8 -*-
import utils
import constants
import pickle
import pdb


def load_utf8_dictionaries():
    for filename in constants.ENTAILMENT_DICTIONARY_NAMES:
        # keyの語 entails valueの語 になる。
        d = dict()
        with open('%s.utf8' % filename, 'r') as f:
            # 'N品登場する N品用意する\n'
            for line in f:
                texts = line.strip().split(' ')
                d[texts[0]] = texts[1]
        with open('%s.pkl' % filename, 'wb') as f:
            pickle.dump(d, f)
            print(d)


if __name__ == '__main__':
    utils.go_to_entailment_dictionaries_dir()
    load_utf8_dictionaries()