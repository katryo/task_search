import constants
import pdb
from entailment_db_data_loader import EntailmentDBDataLoader


class EntailmentLibrarian(object):
    def __init__(self):
        self.dictionary_names = constants.ENTAILMENT_DICTIONARY_TABLENAMES

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

    def entailing_from_all_except_for_nonent_ntriv_with_entailed(self, entailed):
        results = self.entailing_from_all_dictionaries_with_entailed(entailed)
        del(results['nonentailment_ntriv'])
        if results == 'つ':
            pdb.set_trace()
        return results

    def entailed_from_all_dictionaries_with_entailing(self, entailing):
        results = dict()
        for dictionary_name in self.dictionary_names:
            with EntailmentDBDataLoader(table_name=dictionary_name) as loader:
                result = loader.entailed_with_entailing(entailing)
                results[dictionary_name] = result
        return results

if __name__ == '__main__':
    librarian = EntailmentLibrarian()
    print(librarian.entailing_from_all_except_for_nonent_ntriv_with_entailed('受診する'))