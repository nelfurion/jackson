import string
import re
import multiprocessing

from sklearn.externals import joblib
from nltk.corpus import stopwords

from .config import config

corpus_lock = multiprocessing.Lock()

class TopicClassifierLocal:
    PUNCTUATIONS = string.punctuation + '?\n'

    def __init__(self, text_processor, classifier = None):
        self.text_processor = text_processor
        self.classifier = classifier or joblib.load(config['question_classifier'])

    def predict(self, question):
        question = self._remove_punctuation(question)
        tokenized_input = self.text_processor.tokenize(question)
        tagged_words = self.text_processor.get_pos_tags(tokenized_input)
        pos_tags = [pos for word, pos in tagged_words]

        word_stems = []
        for word in tokenized_input:

            # the stopwords corpus needs synchronized requests
            corpus_lock.acquire()
            if word not in stopwords.words('english') \
                    and word not in TopicClassifierLocal.PUNCTUATIONS:
                word_stems.append(self.text_processor.stem(word))

            corpus_lock.release()

        features_string = ' '.join(word_stems) + ' ' + ' '.join(pos_tags)
        features = self.text_processor.vectorize(features_string)

        result = {
            'topic': self.classifier.predict(features)[0]
        }

        return result

    def _remove_punctuation(self, sentence):
        punctuation_exp = '[' + string.punctuation + ']'
        return re.sub(
            punctuation_exp,
            '',
            sentence)