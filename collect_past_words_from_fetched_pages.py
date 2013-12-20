import constants
import utils
import pdb

if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    pages = pages[1:4]
    for page in pages:
        try:
            page.fetch_html()
            page.remove_html_tags()
        except (ValueError, IndexError):
            continue

        page.set_m_words_from_html_body()
    pdb.set_trace()
