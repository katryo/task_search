from web_item import WebItem
ascii_nums = '0 1 2 3 4 5 6 7 8 9'.split(' ')
jp_nums = '０ １ ２ ３ ４ ５ ６ ７ ８ ９'.split(' ')
kanji_nums = '〇 一 二 三 四 五 六 七 八 九 十'.split(' ')
NUM_LIKE_THINGS = ascii_nums.extend(jp_nums).extend(kanji_nums)

STEP_WORDS = 'ステップ 手順 その'.split(' ')


class Labelable(WebItem):
    '''
    HeadingやSentenceが継承する
    '''
    def __init__(self, string):
        self.body = string.strip()
        self.m_body_words = self.to_m_words(self.body)

    def label_ends_with_verb(self):
        if self.m_body_words[-1].type == '動詞':
            self.features['ends_with_verb'] = True

    def label_starts_with_step_word(self):
        if self.is_starting_with_step_word():
            self.features['starts_with_step_word'] = True

    def is_starting_with_step_word(self):
        for w in STEP_WORDS:
            if self.body.startswith(w):
                return True
        return False

    def label_starts_with_num(self):
        if self.is_starting_with_num():
            self.features['starts_with_num'] = True
            # 初期値がFalseなのでFalseのときset不要

    def is_starting_with_num(self):
        for n in NUM_LIKE_THINGS:
            if self.body.startswith(n):
                return True
        return False

