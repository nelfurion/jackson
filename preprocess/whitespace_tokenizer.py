from tokenizer import Tokenizer

class WhiteSpaceTokenizer(object):
    """Simply tokenizes on whitespace."""
    def tokenize(self, text):
        return text.split(' ')
