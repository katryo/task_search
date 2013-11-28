from labelable import Labelable


class Heading(Labelable):
    '''
    heading.features => {'starts_with_num': True, 'has_step_word': False, ...}
    '''

    def __init__(self, string):
        super(__init__)
        self.features = {
            'starts_with_num': False,
            'starts_with_step_word': False,
            'ends_with_verb': False,
            'word_count': len(self.m_body_words)
        }


