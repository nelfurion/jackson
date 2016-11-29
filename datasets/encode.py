import nltk
import numpy

from sklearn.externals import joblib

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif

VECTORIZERS_FOLDER = '../models/vectorizers/'

def encode_data(train_file, test_file, vectorizer_file=None):
    train_features, train_labels, train_sublabels = parse_data(train_file)
    test_features, test_labels, test_sublabels = parse_data(test_file)

    vectorizer = load_or_train_vectorizer(vectorizer_file, train_features)

    train_features = vectorizer.transform(train_features).toarray()
    test_features = vectorizer.transform(test_features).toarray()

    selector = SelectPercentile(f_classif, percentile=100)
    train_features = selector.fit_transform(train_features, train_labels)
    test_features = selector.transform(test_features)

    train_features = numpy.array(train_features)
    train_labels = numpy.array(train_labels)
    train_sublabels = numpy.array(train_sublabels)
    test_features = numpy.array(test_features)
    test_labels = numpy.array(test_labels)
    test_file = numpy.array(test_file)

    return train_features, \
        train_labels, \
        train_sublabels, \
        test_features, \
        test_labels, \
        test_file

def load_or_train_vectorizer(file = None, train_features = None):
    if file:
        return joblib.load(file)

    return train_vectorizer(train_features)

def train_vectorizer(train_features):
    vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        max_df=0.5,
        stop_words='english')

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
