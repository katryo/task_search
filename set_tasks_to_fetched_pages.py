# -*- coding: utf-8 -*-
import utils
import constants
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    for i, page in enumerate(pages):
        page.set_tasks_from_sentences()
        print('%s の %i 番目のページにtasksをセットしました！' % (page.query, i))
    utils.save_all_pages(pages)
