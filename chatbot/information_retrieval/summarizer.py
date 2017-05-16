class Summarizer(object):
    """
        Gets the n most important sentences from a text based on the frequency of their words.
        Uses max_freq, and min_freq for word selection.
        Default args: min_freq=0.2, max_freq=0.8.
    """
    def __init__(self, lemmatizer, tokenizer, sentence_scorer, min_freq=0.1, max_freq=0.9):
        self.lemmatizer = lemmatizer
        self.max_freq = max_freq
        self.min_freq = min_freq
        self.tokenizer = tokenizer
        self.sentence_scorer = sentence_scorer

    def summarize_by_content_frequency(self, sentence_count, articles):
        if sentence_count < 1:
            raise ValueError('Number of sentences must be equal or larger than 1.')

        text = ''
        for article in articles:
            text += article['text']

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

        scored_sentences = self.sentence_scorer.score_sentences_by_word_frequency(text, frequencies)
        best_sentences = self.sentence_scorer.get_best_unique_sentences(scored_sentences, sentence_count)

        return best_sentences

    def summarize_by_input_frequency(self, sentence_count, articles, nj_phrases):
        if sentence_count < 1:
            raise ValueError('Number of sentences must be equal or larger than 1.')

        text = ''
        for article in articles:
            text += ' ' + article['text']

        sentence_scores = self.sentence_scorer.score_sentences_by_input_phrases(text, 'all pages', nj_phrases)

        best_sentences = self.sentence_scorer.get_best_unique_sentences(sentence_scores, sentence_count)

        return best_sentences

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