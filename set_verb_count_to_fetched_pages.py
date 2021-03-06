import utils
import pdb


if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        page.set_text_from_html_body()
        page.set_verb_count()
        page.set_sahen_count()

    whole_verb_count = {}
    whole_sahen_count = {}
    for page in pages:
        for word in page.verb_count:
            if word in whole_verb_count:
                whole_verb_count[word] += 1
                continue
            whole_verb_count[word] = 1

        for word in page.sahen_count:
            if word in whole_sahen_count:
                whole_sahen_count[word] += 1
                continue
            whole_sahen_count[word] = 1

    wc = whole_verb_count
    sc = whole_sahen_count
    pdb.set_trace()
    print([w for w in wc if wc[w] > 2])
