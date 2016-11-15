from interfaces.tokenizer import Tokenizer

class WhiteSpaceTokenizer(object):
    """Simply tokenizes on whitespace."""
    def __init__(self):
        super().__init__()
        pass

    def tokenize(self, text):
        return text.split(' ')
