from mecabed_word import MecabedWord


class MecabedNoun(MecabedWord):
    def __init__(self, word):
        self.name = word
        self.type = '名詞'