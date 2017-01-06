import nltk.stem.snowball

from .stemmer import Stemmer

class SnowballStemmer(Stemmer):
    """Uses default nltk SnowballStemmer."""
    def __init__(self):
        self.stemmer = nltk.stem.snowball.SnowballStemmer("english")

    def stem(self, token):
        return self.stemmer.stem(token)
