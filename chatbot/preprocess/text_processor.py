import numpy
import nltk

class TextProcessor:
    def __init__(self, tokenizer, stemmer, vectorizer, lemmatizer, parser, tagged_words_corpus):
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.vectorizer = vectorizer
        self.lemmatizer = lemmatizer
        self.parser = parser
        self.tagged_words_corpus = tagged_words_corpus

    def tokenize(self, utterance):
        return self.tokenizer.tokenize_words(utterance)

    def tokenize_sentences(self, text):
        return self.tokenizer.tokenize_sentences(text)

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

    def stem(self, word):
        return self.stemmer.stem(word)

    def get_named_entity_chunks(self, tagged_sentences, binary):
        return nltk.ne_chunk_sents(tagged_sentences, binary)

    def get_most_common_usage(self, word):
        return self.tagged_words_corpus.get_most_common_usage(word)

    def parse_to_tree(self, text):
        return self.parser.parse(text)