import utils
import pdb

if __name__ == '__main__':
    d = utils.load_object_term_dictionary()
    for term in d.object_terms:
        term.set_core_noun_from_name()
        print(term.core_noun)
    utils.save_term_dictionary(d)
