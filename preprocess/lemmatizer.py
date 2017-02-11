from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus.reader.wordnet import WordNetError

class Lemmatizer():
    ERROR_FORMAT = 'ERROR in Lemmatizer: {error}, returning {value}'
    LEMMA_KEY_FORMAT = '{word}.{function}'
    SYNSET_KEY_FORMAT = '{lemma}.{function}.01'

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.lemmas_dict = {}
        self.synsets_dict = {}

    def get_lemmas(self, word, function):
        try:
            function = self._translate_function(function)
            synset = wn.synset(word+ '.' + function + '.01')

            if not synset:
                return []

            return synset.lemmas()
        except WordNetError as e:
            return [word]

    def lemmatize(self, word, function):
        try:
            function = self._translate_function(function)
            lemmas = self.lemmatizer.lemmatize(word, function)
            return lemmas
        except WordNetError as e:
            return word

    def get_synonyms(self, word, function, threshold):
        try:
            lemma = self.lemmatizer.lemmatize(word, function)
            default_synset = wn.synset(lemma + '.' + function + '.01')
            synsets = wn.synsets(lemma)
            synonyms = []
            for synset in synsets:

                path_similarity = synset.path_similarity(default_synset)
                if path_similarity\
                        and path_similarity >= threshold\
                        and synset.pos() == function:
                    synset_name = synset.name().split('.')[0]
                    synonyms.append(synset_name)

            return synonyms

        except WordNetError as e:
            return []

    def get_similarity(self, first_word, second_word, function):
        first_word_synset = self._get_synset(first_word, function)
        second_word_synset = self._get_synset(second_word, function)

        if not first_word_synset or not second_word_synset:
            return 0

        return first_word_synset.path_similarity(second_word_synset) or 0

    def _get_synset(self, word, function):
        try:
            lemma = self._get_lemma(word, function)
            synset_key = Lemmatizer.SYNSET_KEY_FORMAT.format(
                lemma=lemma,
                function=function
            )

            if synset_key not in self.synsets_dict.keys():
                self.synsets_dict[synset_key] = wn.synset(synset_key)

        except WordNetError as e:
            self.synsets_dict[synset_key] = None

        return self.synsets_dict[synset_key]

    def _get_lemma(self, word, function):
        key = Lemmatizer.LEMMA_KEY_FORMAT.format(
            word=word,
            function=function
        )

        if key not in self.lemmas_dict.keys():
            try:
                self.lemmas_dict[key] = self.lemmatizer.lemmatize(word, function)
            except WordNetError as e:
                self.lemmas_dict[key] = word

        return self.lemmas_dict[key]

    def _translate_function(self, function):
        functions = {
            'verb': 'v',
            'v': 'v',
            'noun': 'n',
            'n': 'n',
            'adj': 'a',
            'a': 'a',
            'adjective': 'a'
        }

        if function.lower() not in list(functions.keys()):
            raise ValueError('function must be in ', list(functions.keys()))

        return functions.get(function.lower())