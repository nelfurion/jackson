from nltk.data import find
from nltk.parse.bllip import BllipParser

class Parser:
    _instance = None

    def parse(self, tokenized_sentence):
        print(tokenized_sentence)
        return self.parser.parse_one(tokenized_sentence)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            model_dir = find('models/bllip_wsj_no_aux').path
            Parser._instance = BllipParser.from_unified_model_dir(model_dir)

        return Parser._instance