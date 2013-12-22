import pdb

class MecabedWord:
    def __init__(self, word_info):
        tips = word_info.split(',')
        name_and_type = tips[0].split('\t')
        if len(name_and_type) == 1:
            pdb.set_trace()
        name = name_and_type[0]
        type = name_and_type[1]
        self.name = name
        self.type = type
        self.subtype = tips[1]
        self.word_info = word_info

    def __str__(self):
        return self.name

    def is_characteristic_word(self):
        if self.name == "なら" and self.type == "助動詞":
            return True
        if self.name == "で" and self.type == "助詞" and self.subtype == "格助詞":
            return True
        if self.name == "は" and self.type == "助詞" and self.subtype == "係助詞":
            return True
        return False