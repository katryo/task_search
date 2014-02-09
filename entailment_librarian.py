#coding: utf-8
import constants
import pdb
from entailment_db_data_loader import EntailmentDBDataLoader


class EntailmentLibrarian(object):
    def __init__(self):
        self.dictionary_names = constants.ENTAILMENT_DICTIONARY_TABLENAMES
        self.used_results_by_specials = dict()

    def entailing_from_all_dictionaries_with_entailed(self, entailed):
        results = dict()
        for dictionary_name in self.dictionary_names:
            with EntailmentDBDataLoader(table_name=dictionary_name) as loader:
                result = loader.entailing_with_entailed(entailed)
                results[dictionary_name] = result
        return results

    def entailed_from_all_except_for_nonent_ntriv_with_entailing(self, entailing):
        results = self.entailed_from_all_dictionaries_with_entailing(entailing)
        del(results['nonentailment_ntriv'])
        return results

    def genaral_from_all_except_for_nonent_ntriv_with_special(self, entailed):
        if entailed in self.used_results_by_specials:
            print('%sはすでにエンテイルメントを調べていました！' % entailed)
            return self.used_results_by_specials[entailed]
        results = self.entailing_from_all_dictionaries_with_entailed(entailed)
        print('%sのエンテイルメントの調査完了！' % entailed)
        self.used_results_by_specials[entailed] = results
        return results

    def entailed_from_all_dictionaries_with_entailing(self, entailing):
        dicts = dict()
        for dictionary_name in self.dictionary_names:
            with EntailmentDBDataLoader(table_name=dictionary_name) as loader:
                result = loader.entailed_with_entailing(entailing)
                dicts[dictionary_name] = result
        terms = set()
        """
        # dicts => {'nonentailment_anton': [],
        #  'nonentailment_triv': [], 'nonentailment_predi': [],
        #  'entailment_triv': [], 'nonentailment_ntriv': ('掃く',),
        # 'entailment_acrac': [], 'entailment_presu': [],
        #  'entailment_ntriv': ('清掃する',)}
        """
        for dictionary_name in dicts:
            for item in dicts[dictionary_name]:
                terms.add(item)
        return terms  # => {'', '', ...}

if __name__ == '__main__':
    librarian = EntailmentLibrarian()
    print(librarian.entailing_from_all_except_for_nonent_ntriv_with_entailed('受診する'))