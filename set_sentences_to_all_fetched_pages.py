import utils

if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    for i, page in enumerate(pages):
        try:
            page.set_text_from_html_body()
            page.set_sentences_from_text()
            print('%i番目のpageにsentencesセット完了' % i)
        except (ValueError, IndexError):
            continue

    utils.save_all_pages(pages)

