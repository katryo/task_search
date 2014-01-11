import constants
from entailment_db_data_loader import EntailmentDBDataLoader

class EntailmentLibrarian(object):
    def __init__(self):
        self.dictionary_names = constants.ENTAILMENT_DICTIONARY_TABLENAMES

    def entailed_verbs_with_entailing_with_all_dictionaries(self, entailing):
        results = []
        for dictionary_name in self.dictionary_names:
            with EntailmentDBDataLoader(table_name=dictionary_name) as loader:
                result = loader.entailed_verbs_with_entailing(entailing)
                results.append(result)
        return results

if __name__ == '__main__':
    librarian = EntailmentLibrarian()
    print(librarian.entailed_verbs_with_entailing_with_all_dictionaries('体験する'))