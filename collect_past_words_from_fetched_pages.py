import constants
import utils
import pickle
import pdb

if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        sentences_index_with_past_words = []
        for sentence_index, sentence in enumerate(page.sentences):
            m_words = utils.m_words(sentence)

            for i, m_word in enumerate(m_words):
                if m_word.word_info == 'た\t助動詞,*,*,*,特殊・タ,基本形,た,タ,タ':
                    if m_words[i-1].word_info != 'でし\t助動詞,*,*,*,特殊・デス,連用形,です,デシ,デシ' \
                            and m_words[i-1].word_info != 'だっ\t助動詞,*,*,*,特殊・ダ,連用タ接続,だ,ダッ,ダッ':
                        sentences_index_with_past_words.append(sentence_index)

        page.past_sentences = [page.sentences[index] for index in sentences_index_with_past_words]
    for i, page in enumerate(pages):
        with open('%s_%s.pkl' % (constants.FINAL_QUERY, str(i)), 'wb') as f:
            pickle.dump(page, f)
    pdb.set_trace()