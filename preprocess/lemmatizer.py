from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus.reader.wordnet import WordNetError

class Lemmatizer():
    ERROR_FORMAT = 'ERROR in Lemmatizer: {error}, returning {value}'
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def get_lemmas(self, word, function):
        try:
            function = self._translate_function(function)
            synset = wn.synset(word+ '.' + function + '.01')

            if not synset:
                return []

            return synset.lemmas()
        except WordNetError as e:
            print(self.ERROR_FORMAT.format(
                error = e,
                value = [word]
            ))

            return [word]

    def lemmatize(self, word, function):
        try:
            function = self._translate_function(function)
            lemmas = self.lemmatizer.lemmatize(word, function)
            return lemmas
        except WordNetError as e:
            print(self.ERROR_FORMAT.format(
                error = e,
                value = word
            ))

            return word

    def get_synonyms(self, word):
        try:
            default_synset = wn.synset(word)
            synsets = wn.synsets(word)
            for synset in synsets:
                print(synset, ' ', synset.path_similiarity(default_synset))

            return wn.synsets(word)
        except WordNetError as e:
            print(self.ERROR_FORMAT.format(
                error = e,
                value = []
            ))

            return []


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