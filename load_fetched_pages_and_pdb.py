import constants
import utils
import pickle
import pdb

if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        print(page.past_sentences)