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

        if len(text) < 1:
            raise ValueError('Can\t summarize on empty text.')

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

        scored_sentences = self._score_sentences_by_word_frequency(tokenized_sentences, frequencies)
        best_sentences = self._get_best_unique_sentences(scored_sentences, sentence_count)

        return best_sentences

    def summarize_by_input_frequency(self, sentence_count, text, nj_phrases):
        if sentence_count < 1:
            raise ValueError('Number of sentences must be equal or larger than 1.')

        tokenized_sentences = self._tokenize_sentences(text)
        sentence_scores = self._score_sentences_by_input_phrases(tokenized_sentences, nj_phrases)
        best_sentences = self._get_best_unique_sentences(sentence_scores, sentence_count)

        return best_sentences

    def _get_best_unique_sentences(self, scored_sentences, sentence_count):
        used_sentences = []
        sentence_tuples = []
        index = 0
        while(len(used_sentences) < sentence_count):
            score_tuple = scored_sentences[index]
            sentence_order_in_text = score_tuple[1]
            tokenized_sentence = score_tuple[0]

            sentence_end = tokenized_sentence[-2] + tokenized_sentence[-1]
            full_sentence = ' '.join(tokenized_sentence[0:-2]) + ' ' + sentence_end

            if full_sentence not in used_sentences:
                used_sentences.append(full_sentence)
                sentence_and_order = (full_sentence, sentence_order_in_text)
                sentence_tuples.append(sentence_and_order)

            index += 1

        ordered_by_appearance = sorted(sentence_tuples, key=lambda x: x[1])
        sentences = [order_tuple[0] for order_tuple in ordered_by_appearance]

        return sentences

    def _get_similarity(self, keyword, word, function):
        if keyword in self.similarity_dict.keys():
            if word in self.similarity_dict[keyword].keys():
                return self.similarity_dict[keyword][word]
            else:
                similarity = self.lemmatizer.get_similarity(keyword, word, function)
                self.similarity_dict[keyword][word] = similarity

                return similarity
        else:
            similarity = self.lemmatizer.get_similarity(keyword, word, function)
            self.similarity_dict[keyword] = {
                word: similarity
            }

            return similarity

    def _tokenize_sentences(self, text):
        sentences = self.tokenizer.tokenize_sentences(text)
        final_sentences = []

        for sentence in sentences:
            last_index = -1
            should_add_sentence = True
            for i in range(len(sentence)):
                if sentence[i] == '\n':
                    if last_index == -1:
                        last_index = i
                    elif i - last_index == 1:
                        last_index = i
                    else:
                        should_add_sentence = False

            if should_add_sentence:
                final_sentences.append(sentence)

        return [
            self.tokenizer.tokenize_words(sentence)
            for sentence in final_sentences
        ]

    def _score_sentences_by_word_frequency(self, tokenized_sentences, word_frequencies):
        sentence_scores = []
        for i in range(len(tokenized_sentences)):
            score = 0
            for word in tokenized_sentences[i]:
                if word in word_frequencies:
                    score += word_frequencies[word]

            sentence_scores.append((tokenized_sentences[i], i, score))

        sentence_scores = sorted(sentence_scores, key=lambda x: x[2])
        sorted_descending = list(reversed(sentence_scores))

        return sorted_descending

    def _score_sentences_by_input_phrases(self, tokenized_sentences, nj_phrases):
        nouns_count = len(nj_phrases['nouns'])
        adjectives_count = len(nj_phrases['adjectives'])
        sentence_scores = []
        for i in range(len(tokenized_sentences)):
            if len(tokenized_sentences[i]) > 1:
                # This is the minimal length for a complete sentence.
                sentence_score = 0
                nouns_found = set()
                adjectives_found = set()

                for word in tokenized_sentences[i]:
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

                    for char in word:
                        if char == '=':
                            sentence_score -= 10


                sentence_score += len(adjectives_found) + len(nouns_found)
                sentence_scores.append((tokenized_sentences[i], i, sentence_score))

        sentence_scores = sorted(sentence_scores, key=lambda x: x[2])
        sorted_descending = list(reversed(sentence_scores))

        return sorted_descending