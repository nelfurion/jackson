import numpy
import nltk

class TextProcessor:
    def __init__(self, tokenizer, stemmer, vectorizer, lemmatizer):
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.vectorizer = vectorizer
        self.lemmatizer = lemmatizer

    def tokenize(self, utterance):
        return self.tokenizer.tokenize_words(utterance)

    def vectorize(self, utterance):
        vector = self.vectorizer.transform([utterance]).toarray()

        return numpy.array(vector)

    def get_lemmas(self, word, function):
        return self.lemmatizer.get_lemmas(word, function)

    def lemmatize(self, word, function):
        return self.lemmatizer.lemmatize(word, function)

    def get_synonyms(self, word, function, threshold):
        return self.lemmatizer.get_synonyms(word, function, threshold)

    def get_word_similarity(self, first, first_function, second, second_function):
        return self.lemmatizer.get_word_similarity(first, first_function, second, second_function)

    def get_pos_tags(self, tokenized_sentence):
        return nltk.pos_tag(tokenized_sentence)