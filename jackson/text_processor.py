import numpy

class TextProcessor:
    def __init__(self, tokenizer, stemmer, vectorizer):
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.vectorizer = vectorizer

    def process(self, utterance):
        tokens = self.tokenizer.tokenize(utterance)
        for i in range(len(tokens)):
            tokens[i] = self.stemmer.stem(tokens[i])

        utterance = ' '.join(tokens)

    def vectorize(self, utterance):
        vector = self.vectorizer.transform([utterance]).toarray()
        return numpy.array(vector)