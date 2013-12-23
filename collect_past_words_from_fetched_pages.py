import constants
import utils
import pickle
import pdb
import re

def text_without_breaks(text):
    break_pattern_n = re.compile('\n')
    break_pattern_r = re.compile('\r')
    tab_pattern = re.compile('\t')
    whitespace_pattern = re.compile('\\u3000')
    text = break_pattern_n.sub('', text)
    text = break_pattern_r.sub('', text)
    text = tab_pattern.sub('', text)
    text = whitespace_pattern.sub('', text)
    return text

def has_past(i, m_word, m_words):
    if m_word.word_info == 'た\t助動詞,*,*,*,特殊・タ,基本形,た,タ,タ':
        if m_words[i-1].word_info != 'でし\t助動詞,*,*,*,特殊・デス,連用形,です,デシ,デシ' \
        and m_words[i-1].word_info != 'だっ\t助動詞,*,*,*,特殊・ダ,連用タ接続,だ,ダッ,ダッ':
            return True
        return False

def has_too_many_whitespaces(text):
    num_of_whitespaces = text.count(' ')
    if num_of_whitespaces / len(text) > 0.5:
        return True
    return False

def set_past_sentences(page):
    page.past_sentences = []
    sentence_indexes = [{'sentence_i': 0, 'past_word_i':0}]
    for sentence_index, sentence in enumerate(page.sentences):
        m_words = utils.m_words(sentence)

        for i, m_word in enumerate(m_words):
            # iはm_wordに分けたあとの順番
            if has_past(i, m_word, m_words) and not has_too_many_whitespaces(sentence):
                sentence_indexes.append({'sentence_i': sentence_index, 'past_word_i':i})
                before_past_word = ''.join([m_word.name for j, m_word in enumerate(m_words) if j < i + 1])
                result = text_without_breaks(before_past_word)
                page.past_sentences.append(result)


if __name__ == '__main__':
    pages = utils.load_fetched_pages()
    for page in pages:
        set_past_sentences(page)
    for i, page in enumerate(pages):
        with open('%s_%s.pkl' % (constants.FINAL_QUERY, str(i)), 'wb') as f:
            pickle.dump(page, f)
