'''
TODO:
There are a number of wrong thing in this file...
'''

import nltk

import numpy

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.externals import joblib

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

def encode_data(train_file, test_file):
    train_features, train_labels, train_sublabels = parse_data(train_file)
    test_features, test_labels, test_sublabels = parse_data(test_file)

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')

    train_features = vectorizer.fit_transform(train_features).toarray()
    test_features = vectorizer.transform(test_features).toarray()

    selector = SelectPercentile(f_classif, percentile=100)
    train_features = selector.fit_transform(train_features, train_labels)
    test_features = selector.transform(test_features)

    joblib.dump(vectorizer, 'vectorizer.pkl')
    return numpy.array(train_features), numpy.array(train_labels), numpy.array(train_sublabels), numpy.array(test_features), numpy.array(test_labels), numpy.array(test_file)

train_features, train_labels, train_sublabels, test_features, test_labels, test_sublabels = encode_data('../questions.txt', '../test_questions.txt')

classifier = GaussianNB()
classifier.fit(train_features, train_labels)
predictions = classifier.predict(test_features)

correct_count = 0
for i in range(len(predictions)):
    if predictions[i] == test_labels[i]:
        correct_count += 1

accuracy = correct_count / len(predictions)

print("accuracy: ", accuracy)

joblib.dump(classifier, './classifiers/question_naive_bayes_no_params_' + str(accuracy) + '.pkl')
