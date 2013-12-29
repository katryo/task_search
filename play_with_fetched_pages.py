import utils
import patterns
import pdb


if __name__ == '__main__':
    pages = utils.load_all_fetched_pages()
    for page in pages:
        for sentence in page.sentences:
            for direction in patterns.directions:
                if direction in sentence:
                    #point_of_direction = sentence.index(direction)
                    #sahens = utils.sahens_or_verbs(sentence[point_of_direction-10:point_of_direction])
                    results = page.target_and_action_by_wo_from_sentences()
                    result_set = set(results)
                    if results:
                        print(result_set)

