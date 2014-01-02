import utils
import pdb

if __name__ == '__main__':
    object_term_dictionary = utils.load_object_term_dictionary()
    pages = utils.load_all_fetched_pages()
    for page in pages:
        for task in page.tasks:
            object_term_dictionary.add(task.object_term)
    pdb.set_trace()