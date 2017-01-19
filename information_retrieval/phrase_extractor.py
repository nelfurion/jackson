import nltk
from nltk.corpus import brown

class PhraseExtractor:
    def extract(self, tree):
        nouns = self._extract_nouns(tree)
        adjectives = self._extract_adjectives(tree)

        return nouns, adjectives

    def _is_used_as_noun(self, text):
        if len(text) == 1:
            if text[-3:] == 'est':
                most_common_usage = self._get_most_common_usage(text)
                print(most_common_usage, ' for word ', text)

                return 'NN' in most_common_usage[0]
        else:
            if text[-3:] == 'est':
                return False

        return True

    def _extract_nouns(self, tree):
        nouns = set()
        noun_phrases = set()
        for node in tree:
            if hasattr(node, 'label'):
                node_text = ' '.join(node.leaves())
                node_label = node.label()

                if 'NN' in node_label\
                        and self._is_used_as_noun(node_text):
                    print('APPENDING: ', node_text)
                    nouns.add(node_text)
                if node_label == 'NP'\
                        and self._is_used_as_noun(node_text):
                    print('APPENDING: ', node_text)
                    noun_phrases.add(node_text)

                nouns_and_phrases = self._extract_nouns(node)
                nouns.update(nouns_and_phrases[0])
                noun_phrases.update(nouns_and_phrases[1])

        return nouns, noun_phrases

    def _extract_adjectives(self, tree):
        adjectives = set()
        adjective_phrases = set()
        for node in tree:
            if hasattr(node, 'label'):
                node_label = node.label()
                node_text = ' '.join(node.leaves())

                if node_label == 'ADJP':
                    adjective_phrases.add(node_text)
                    print('APPENDING: ', node_text)
                if 'JJ' in node_label:
                    adjectives.add(node_text)
                    print('APPENDING: ', node_text)

                adjectives_and_phrases = self._extract_adjectives(node)
                adjectives.update(adjectives_and_phrases[0])
                adjective_phrases.update(adjectives_and_phrases[1])

        return adjectives, adjective_phrases

    def _get_most_common_usage(self, word):
        return nltk.FreqDist(t for w, t in brown.tagged_words() if w.lower() == word).most_common(1)