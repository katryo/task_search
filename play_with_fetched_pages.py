import utils
import patterns


if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        for sentence in page.sentences:
            for direction in patterns.directions:
                if direction in sentence:
                    print(sentence)
