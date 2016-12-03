import nltk
import numpy

from sklearn.externals import joblib

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif

VECTORIZERS_FOLDER = '../models/vectorizers/'

def encode_data(file, vectorizer):
    features, labels, sublabels = parse_data(file)
    features = vectorizer.transform(features).toarray()

    return (features, labels, sublabels)

def load_or_train_vectorizer(vectorizer = None, train_features = None):
    if type(vectorizer) is str:
        return joblib.load(vectorizer)

    return train_vectorizer(train_features)

def train_vectorizer(train_features):
    vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 3))

    vectorizer.fit(train_features)

    vectorizer_name = vectorizer.__class__.__name__
    file_name = VECTORIZERS_FOLDER + vectorizer_name + '.pkl'
    joblib.dump(vectorizer, file_name)

    return vectorizer

def parse_data(file, stemmer=SnowballStemmer("english")):
    features = []
    labels = []
    sublabels = []

    with open(file) as f:
        content = f.readlines()
        for line in content:
            parts = line.split(' ', 1)
            question = parts[1]
            question_types = parts[0].split(':')
            main_type = question_types[0]
            subtype = question_types[1]

            words = [word for word in question.split(' ') if word not in stopwords.words('english')]
            for i in range(len(words)):
                words[i] = stemmer.stem(words[i])

            question = ' '.join(words)

            labels.append(main_type)
            sublabels.append(subtype)
            features.append(question)

    return features, labels, sublabels

def get_vectorizer_weights(vectorizer, features):
    weights = dict(zip(vectorizer.get_feature_names(), features.data))
    return weights

def print_to_file(text, action):
    with open("output.txt", action) as myfile:
        myfile.write(str(text))
