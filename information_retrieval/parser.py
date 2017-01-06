from nltk.data import find
from nltk.parse.bllip import BllipParser

class Parser:
    def __init__(self):
        model_dir = find('models/bllip_wsj_no_aux').path
        self.parser = BllipParser.from_unified_model_dir(model_dir)

    def parse(self, tokenized_sentence):
        return self.parser.parse_one(tokenized_sentence)
