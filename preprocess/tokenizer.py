from decorators.abstract_method import abstract_method

class Tokenizer:
    @abstract_method
    def tokenize(self, text):
        pass
