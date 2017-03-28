import nltk

class Tokenizer:
    def tokenize_words(self, text):
        return nltk.word_tokenize(text)

    def tokenize_sentences(self, text):
        return nltk.sent_tokenize(text)
