import utils


if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        page.set_past_word_count()
