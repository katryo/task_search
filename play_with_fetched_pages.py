import utils
import patterns
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    # pdb.set_trace()
    for i, page in enumerate(pages):
        results = page.obj_and_verb_list_by_wo_from_sentences()
        if results:
            print(results)
            print('%i番目のWebPage' % i)
