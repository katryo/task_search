# -*- coding: utf-8 -*-
import utils
import constants
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    dictionaries = utils.load_entailment_dictionaries()
    for page in pages:
        for task in page.tasks:
            # print('%s, %s' % (task.object_term.name, task.object_term.context))
            for dictionary in dictionaries:
                if task.predicate_term in dictionaries[dictionary]:
                    entailed_or_entailings = dictionaries[dictionary][task.predicate_term]
                    for entailed_or_entailing in entailed_or_entailings:
                        # 多すぎる……！ SQLiteに保存せねば
                        print('%s %s %s entails %s %s %s' % (
                            task.object_term.name,
                            task.cmp,
                            task.predicate_term,
                            task.object_term.name,
                            task.cmp,
                            entailed_or_entailing
                        )
                        )
