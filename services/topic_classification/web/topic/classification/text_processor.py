import numpy
import nltk

from sklearn.externals import joblib
from .config import config

class TextProcessor:
    def __init__(self, stemmer, tokenizer, vectorizer = None):
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.vectorizer = vectorizer or joblib.load(config['vectorizer'])

    def vectorize(self, utterance):
        vector = self.vectorizer.transform([utterance]).toarray()

        return numpy.array(vector)

    def get_pos_tags(self, tokenized_sentence):
        return nltk.pos_tag(tokenized_sentence)

    def stem(self, word):
        return self.stemmer.stem(word)

    def tokenize(self, utterance):
        return self.tokenizer.tokenize_words(utterance)
