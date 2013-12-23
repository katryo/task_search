import utils
import pdb


if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        page.set_past_word_count()

    whole_past_word_count = {}
    for page in pages:
        for word in page.past_word_count:
            if word in whole_past_word_count:
                whole_past_word_count[word] += 1
                continue
            whole_past_word_count[word] = 1

    wc = whole_past_word_count
    pdb.set_trace()
    print([w for w in wc if wc[w] > 2])
