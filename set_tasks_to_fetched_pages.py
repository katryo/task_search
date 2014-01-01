# -*- coding: utf-8 -*-
import utils
import constants
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    for page in pages:
        page.set_tasks_from_sentences()
    utils.save_all_pages(pages)
