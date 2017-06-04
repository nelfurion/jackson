import string
import re

from sklearn.externals import joblib
from nltk.corpus import stopwords

from .config import config

class TopicClassifierLocal:
    PUNCTUATIONS = string.punctuation + '?\n'

    def __init__(self, text_processor, classifier = None):
        self.text_processor = text_processor
        self.classifier = classifier or joblib.load(config['question_classifier'])

    def classify(self, question):
        question = self._remove_punctuation(question)
        tokenized_input = self.text_processor.tokenize(question)
        tagged_words = self.text_processor.get_pos_tags(tokenized_input)
        pos_tags = [pos for word, pos in tagged_words]

        word_stems = []
        for word in tokenized_input:
            if word not in stopwords.words('english') \
                    and word not in TopicClassifierLocal.PUNCTUATIONS:
                word_stems.append(self.text_processor.stem(word))

        features_string = ' '.join(word_stems) + ' ' + ' '.join(pos_tags)
        features = self.text_processor.vectorize(features_string)

        return self.classifier.predict(features)

    def _remove_punctuation(self, sentence):
        print(type(sentence))
        punctuation_exp = '[' + string.punctuation + ']'
        print(type(punctuation_exp))
        return re.sub(
            punctuation_exp,
            '',
            sentence)