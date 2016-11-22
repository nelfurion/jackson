from nltk.corpus import stopwords
from string import punctuation

class Summarizer(object):
    """
        Gets the n most important sentences from a text based on the frequency of their words.
        Uses max_freq, and min_freq for word selection.
    """
    def __init__(self, min_freq, max_freq):
        self.max_freq = max_freq
        self.min_freq = min_freq

    def summarize(self, n, tokenized_sentences):
        if n < 1:
            raise ValueError('Number of sentences must be equal or larger than 1.')

        appearances = {}
        for sentence in tokenized_sentences:
            for word in sentence:
                if word in appearances:
                    appearances[word] += 1
                else:
                    appearances[word] = 1

        max_appearances = appearances[max(appearances, key=lambda k: appearances[k])]


        frequencies = {}
        for word in appearances:
            frequency = appearances[word] / max_appearances
            if frequency <= self.max_freq and frequency >= self.min_freq:
                frequencies[word] = frequency
                print(frequency)

        return self._get_sentences(n, tokenized_sentences, frequencies)

    def _get_sentences(self, n, tokenized_sentences, word_frequencies):
        sentence_scores = []
        for i in range(len(tokenized_sentences)):
            score = 0
            for word in tokenized_sentences[i]:
                if word in word_frequencies:
                    score += word_frequencies[word]

            sentence_scores.append((tokenized_sentences[i], i, score))

        sentence_scores = list(reversed(sorted(sentence_scores, key=lambda x: x[2])))

        print(sentence_scores)

        return [x[0] for x in sentence_scores[:n]]
