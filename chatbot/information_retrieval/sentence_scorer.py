import information_retrieval.utils as utils

class SentenceScorer:
    DEFAULT_SIMILARITY = 0.1

    def __init__(self, text_processor, phrase_extractor):
        self.similarity_dict = {}
        self.text_processor = text_processor
        self.phrase_extractor = phrase_extractor

    def score_sentences_by_word_frequency(self, text, word_frequencies):
        tokenized_sentences = utils.tokenize_sentences(self.text_processor.tokenizer, text)
        sentence_scores = []
        for i in range(len(tokenized_sentences)):
            score = 0
            for word in tokenized_sentences[i]:
                if word in word_frequencies:
                    score += word_frequencies[word]

            sentence_scores.append((tokenized_sentences[i], i, score))

        return sentence_scores

    def score_sentences_by_input_phrases(self, text, title, nj_phrases):
        tokenized_sentences = utils.tokenize_sentences(self.text_processor.tokenizer, text)
        nouns_count = len(nj_phrases['nouns'])
        adjectives_count = len(nj_phrases['adjectives'])
        sentence_scores = []

        phrase_word_tuples = []

        for adjective in nj_phrases['adjectives']:
            lem_tuple = (adjective, 'a')
            phrase_word_tuples.append(lem_tuple)

        for noun in nj_phrases['nouns']:
            lem_tuple = (noun, 'n')
            phrase_word_tuples.append(lem_tuple)

        for i in range(len(tokenized_sentences)):
            if len(tokenized_sentences[i]) > 1:
                # This is the minimal length for a complete sentence.
                sentence_score = 0
                nouns_found = set()
                adjectives_found = set()

                for word in tokenized_sentences[i]:
                    for phrase_word_tuple in phrase_word_tuples:
                        phrase_word = phrase_word_tuple[0]
                        pos_tag = phrase_word_tuple[1]

                        similarity = self._get_similarity(phrase_word, word, pos_tag) - 0.1
                        sentence_score += similarity
                        if similarity >= 0:
                            if pos_tag == 'a' and len(adjectives_found) < adjectives_count:
                                adjectives_found.add(phrase_word)
                            elif pos_tag == 'n' and len(nouns_found) < nouns_count:
                                nouns_found.add(phrase_word)

                sentence_score += len(adjectives_found) + len(nouns_found)
                sentence_scores.append((tokenized_sentences[i], i, sentence_score))

        return sentence_scores

    def _get_similarity(self, keyword, word, wn_pos):
        if keyword in self.similarity_dict.keys():
            if word in self.similarity_dict[keyword].keys():
                return self.similarity_dict[keyword][word]
            else:
                similarity = self.text_processor.get_word_similarity(keyword, word, wn_pos)
                self.similarity_dict[keyword][word] = similarity

                return similarity
        else:
            similarity = self.text_processor.get_word_similarity(keyword, word, wn_pos)
            self.similarity_dict[keyword] = {
                word: similarity
            }

            return similarity

    def get_best_unique_sentences(self, scored_sentences, sentence_count):
        scored_sentences = sorted(scored_sentences, key=lambda x: x[2])
        scored_sentences = list(reversed(scored_sentences))

        # print('ORDERED BY SCORE')
        # print(scored_sentences[0:10])

        used_sentences = []
        sentence_tuples = []
        index = 0

        while(len(used_sentences) < sentence_count
              and index < len(scored_sentences)):
            score_tuple = scored_sentences[index]
            sentence_order_in_text = score_tuple[1]
            tokenized_sentence = score_tuple[0]

            # print('-' * 30)
            # print(tokenized_sentence)

            sentence_end = tokenized_sentence[-2] + tokenized_sentence[-1]
            print(sentence_end)
            full_sentence = ' '.join(tokenized_sentence[0:-2]) + ' ' + sentence_end
            print('-' * 30)

            if full_sentence not in used_sentences:
                used_sentences.append(full_sentence)
                sentence_and_order = (full_sentence, sentence_order_in_text)
                sentence_tuples.append(sentence_and_order)

            index += 1

        ordered_by_appearance = sorted(sentence_tuples, key=lambda x: x[1])
        sentences = [order_tuple[0] for order_tuple in ordered_by_appearance]

        return sentences

    def score_titles(self, titles, query_nva):
        title_scores = []
        for title in titles:
            title_nva = self.get_title_phrases(title)

            score, matches = self.score_title(title_nva, query_nva)
            title_scores.append((title, score, matches))

        most_matches = sorted(title_scores, key=lambda x: (
            x[2],
            x[1]))
        descending_matches = list(reversed(most_matches))
        print('TITLES BY MATCHES:')
        print(descending_matches)

        title_scores = sorted(title_scores, key=lambda x: x[1])
        descending_scores = list(reversed(title_scores))

        return descending_scores

    def get_title_phrases(self, title):
        tokenized_title = self.text_processor.tokenize_words(title)
        tree = self.text_processor.parse_to_tree(tokenized_title)
        title_nva = self.phrase_extractor.extract(tree)

        return title_nva

    def score_title(self, title_nva, query_nva):
        matches = 0
        score = 1.0

        if 'nouns' in query_nva.keys() and 'nouns' in title_nva.keys():
            nouns_score, noun_matches = self.calculate_words_similarity_score(
                query_nva['nouns'],
                title_nva['nouns'],
                'n')

            score *= nouns_score
            matches += noun_matches

        if 'verbs' in query_nva.keys() \
                and 'verbs' in title_nva.keys() \
                and len(title_nva['verbs']) > 0:
            verbs_score, verb_matches = self.calculate_words_similarity_score(
                query_nva['verbs'],
                title_nva['verbs'],
                'v')

            score *= verbs_score
            matches += verb_matches

        if 'adjectives' in query_nva.keys() and 'adjectives' in title_nva.keys():
            adjectives_score, adj_matches = self.calculate_words_similarity_score(
                query_nva['adjectives'],
                title_nva['adjectives'],
                'a')

            score *= adjectives_score
            matches += adj_matches

        return score, matches

    def calculate_words_similarity_score(self, query_words, title_words, part_of_speech):
        # print('SCORING ', part_of_speech, ' -----')
        matches = 0
        score = 1
        matched_words = set()

        for query_word in query_words:
            for title_word in title_words:
                query_word = query_word.lower()
                title_word = title_word.lower()

                similarity = self.text_processor.get_word_similarity(query_word, title_word, part_of_speech)
                if similarity == 1.0:
                    matches += 1
                    matched_words.add(title_word)
                    matched_words.add(query_word)
                    break

        unmatched_query_words = [word for word in query_words if word.lower() not in matched_words]
        unmatched_title_words = [word for word in title_words if word.lower() not in matched_words]

        unmatched_query_words_length = len(unmatched_query_words)
        unmatched_title_words_length = len(unmatched_title_words)
        length_difference = unmatched_title_words_length - unmatched_query_words_length
        if length_difference > 0:
            score *= pow(0.1, length_difference)

        if unmatched_query_words_length != 0 and unmatched_title_words_length != 0:
            for query_word in unmatched_query_words:
                max_similarity = 0
                for title_word in unmatched_title_words:
                    query_word = query_word.lower()
                    title_word = title_word.lower()
                    similarity = self.text_processor.get_word_similarity(query_word, title_word, part_of_speech)
                    max_similarity = max(max_similarity, similarity)

                    if similarity > 0:
                        score = round(score * similarity, 300)

                if max_similarity == 0:
                    score *= __class__.DEFAULT_SIMILARITY

        return score, matches
