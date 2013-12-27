import constants
import utils
import pdb
import pickle

if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        try:
            page.fetch_html()
            page.set_text_from_html_body()
            page.sentences = utils.split_by_dots(page.text)
        except (ValueError, IndexError):
            continue

    for i, page in enumerate(pages):
        with open('%s_%s.pkl' % (constants.FINAL_QUERY, str(i)), 'wb') as f:
            pickle.dump(page, f)
