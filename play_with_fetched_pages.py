import utils
import patterns
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    for page in pages:
        print(page.obj_and_verb_list_by_wo_from_sentences())

