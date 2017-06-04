import nltk
from nltk.corpus import brown

class TaggedWordsCorpus():
    def get_most_common_usage(self, word):
        return nltk.FreqDist(
                word_type for word, word_type in brown.tagged_words()
                if word.lower() == word)\
            .most_common(1)