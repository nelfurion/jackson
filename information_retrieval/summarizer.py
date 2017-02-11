from preprocess.tokenizer import Tokenizer
tokenizer = Tokenizer()

class Summarizer(object):
    """
        Gets the n most important sentences from a text based on the frequency of their words.
        Uses max_freq, and min_freq for word selection.
        Default args: min_freq=0.2, max_freq=0.8.
    """
    def __init__(self,lemmatizer, tokenizer = tokenizer, min_freq=0.1, max_freq=0.9):
        self.lemmatizer = lemmatizer
        self.max_freq = max_freq
        self.min_freq = min_freq
        self.tokenizer = tokenizer
        self.similarity_dict = {}

    def summarize(self, sentence_count, text):
        if sentence_count < 1:
            raise ValueError('Number of sentences must be equal or larger than 1.')

        tokenized_sentences = self._tokenize_sentences(text)

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

        top_sentences = self._get_sentences(sentence_count, tokenized_sentences, frequencies)
        top_sentences = [' '.join(sentence) for sentence in top_sentences]

        return top_sentences

    def summarize_by_input_frequency(self, sentence_count, text, nj_phrases):
        if sentence_count < 1:
            raise ValueError('Number of sentences must be equal or larger than 1.')

        nouns_count = len(nj_phrases['nouns'])
        adjectives_count = len(nj_phrases['adjectives'])

        sentence_scores = []
        tokenized_sentences = self._tokenize_sentences(text)

        for sentence in tokenized_sentences:
            if len(sentence) > 1:
                # This is the minimal length for a complete sentence.
                sentence_score = 0
                nouns_found = set()
                adjectives_found = set()

                for word in sentence:
                    for adjective in nj_phrases['adjectives']:
                        similarity = self._get_similarity(adjective, word, 'a') - 0.1
                        sentence_score += similarity

                        if similarity >= 0 and len(adjectives_found) < adjectives_count:
                            adjectives_found.add(adjective)

                    for noun in nj_phrases['nouns']:
                        similarity = self._get_similarity(noun, word, 'n') - 0.1
                        sentence_score += similarity

                        if similarity >= 0 and len(nouns_found) < nouns_count:
                            nouns_found.add(noun)

                sentence_score += len(adjectives_found) + len(nouns_found)

                sentence_end = sentence[-2] + sentence[-1]
                full_sentence = ' '.join(sentence[0:-2]) + ' ' + sentence_end

                for character in full_sentence:
                    if character == '=':
                        sentence_score -= 1

                sentence_scores.append((full_sentence, sentence_score))

        sentence_scores = sorted(sentence_scores, key=lambda x: x[1])
        best_scores = sentence_scores[-sentence_count:]
        best_sentences = [x[0] for x in best_scores]

        return best_sentences

    def _get_similarity(self, keyword, word, function):
        if keyword in self.similarity_dict.keys():

            if word in self.similarity_dict[keyword].keys():
                return self.similarity_dict[keyword][word]
            else:
                similarity = self.lemmatizer.get_similarity(keyword, word, function)
                self.similarity_dict[keyword][word] = similarity

                return similarity
        else:
            print('KEYWORD ', keyword, " NOT IN DICTIONARY")
            similarity = self.lemmatizer.get_similarity(keyword, word, function)
            self.similarity_dict[keyword] = {
                word: similarity
            }

            print(self.similarity_dict)

            return similarity

    def _tokenize_sentences(self, text):
        sentences = self.tokenizer.tokenize_sentences(text)
        final_sentences = []

        for sentence in sentences:
            last_index = -1
            should_add = True
            for i in range(len(sentence)):
                if sentence[i] == '\n':
                    if last_index == -1:
                        last_index = i
                    elif i - last_index == 1:
                        last_index = i
                    else:
                        should_add = False

            if should_add:
                final_sentences.append(sentence)

        return [
            self.tokenizer.tokenize_words(sentence)
            for sentence in final_sentences
        ]

    def _get_sentences(self, n, tokenized_sentences, word_frequencies):
        sentence_scores = []
        for i in range(len(tokenized_sentences)):
            score = 0
            for word in tokenized_sentences[i]:
                if word in word_frequencies:
                    score += word_frequencies[word]

            sentence_scores.append((tokenized_sentences[i], i, score))

        sentence_scores = sorted(sentence_scores, key=lambda x: x[2])
        ordered_sentences = sorted(sentence_scores[-n:], key=lambda x: x[1])

        return [x[0] for x in ordered_sentences]
