#coding: utf-8
import constants
from sentence import Sentence
from task_data_inserter import TaskDataInserter
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from sentence_data_loader import SentenceDataLoader
import sqlite3
import pdb

if __name__ == '__main__':
    pfl = PickleFileLoaderForOriginal()
    di = TaskDataInserter()
    loader = SentenceDataLoader()
    for i_sentence in range(450000):
        try:
            body = loader.body_with_id(i_sentence+1)
        except EOFError:
            continue
        if not body:
            continue
        sentence = Sentence(body, 'a')
        if sentence.set_noun_verb_if_good_task():
            di.insert(noun=sentence.noun, cmp=sentence.cmp, verb=sentence.verb, sentence_id=i_sentence+1)

