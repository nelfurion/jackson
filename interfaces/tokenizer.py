from decorators.abstract_method import abstract_method

class Tokenizer:
    def __init__(self):
        pass

    @abstract_method
    def tokenize(self, text):
        pass
