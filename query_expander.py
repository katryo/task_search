from entailment_librarian import EntailmentLibrarian
from hypohype_db_data_loader import HypoHypeDBDataLoader
import constants
import pdb


class QueryExpander(object):
    def __init__(self, query_noun, query_verb):
        self.original_query_noun = query_noun
        self.original_query_verb = query_verb

    def hypernym(self):
        hhdbdl = HypoHypeDBDataLoader(db_name='hyponym_hypernym.sqlite', table_name='all_hyponymy')
        results = hhdbdl.select_hypes_with_hypo(self.original_query_noun)
        for result in results:
            for stopword in constants.STOPWORDS_OF_HYPOHYPE:
                if stopword in result:
                    results.remove(result)
        return results

    def entailing(self):
        eddl = EntailmentLibrarian()
        results = eddl.entailing_from_all_except_for_nonent_ntriv_with_entailed(self.original_query_verb)
        return results

    def entailed(self):
        eddl = EntailmentLibrarian()
        results = eddl.entailed_from_all_except_for_nonent_ntriv_with_entailing(self.original_query_verb)
        return results

if __name__ == '__main__':
    qe = QueryExpander('胃もたれ', '防止する')
    print(qe.entailed())
    print(qe.hypernym())
