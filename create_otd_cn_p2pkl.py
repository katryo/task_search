import utils
import pdb

if __name__ == '__main__':
    d = utils.load_object_term_dictionary()
    core_nouns = [t.core_noun for t in d.object_terms]
    utils.save_term_dictionary_with_protocol_2(core_nouns)
