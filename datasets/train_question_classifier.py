'''
TODO:
There are a number of wrong thing in this file...
'''
import numpy

from config import config

import encode

#Importing classifiers
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_accuracy(predictions, test_labels):
    correct_count = 0
    for i in range(len(predictions)):
        if predictions[i] == test_labels[i]:
            correct_count += 1

    return correct_count / len(predictions)

def save_classifier(classifier_name, accuracy, parameters = None):
    file_name = 'q_clf_' + classifier_name + '_'
    if parameters:
        for key, value in parameters.items():
            file_name += str(key) + '='
            file_name += str(value) + '_'

    file_name += 'accuracy=' + str(accuracy)
    file_name += '.pkl'

    joblib.dump(classifier, '../models/classifiers/' + file_name)

encoded_train_data = encode.encode_data(encode.parse_data('./questions_train.txt'))
encoded_test_data = encode.encode_data(encode.parse_data('./questions_test.txt'))

vectorizer = encode.load_or_train_vectorizer(
    vectorizer = TfidfVectorizer(
        ngram_range = (1, 3),
        analyzer = 'word'),
    train_features = encoded_train_data['features'],
    save_file_name = 'MultinomialNBVectorizer')

train_features, train_labels, train_sublabels = encode.transform_data(encoded_train_data, vectorizer)
test_features, test_labels, test_sublabels = encode.transform_data(encoded_test_data, vectorizer)

print(train_features)

for i, model in enumerate(config['models']):
    print('='*30)

    paramter_combinations = config['models_parameters']
    if len(paramter_combinations) > i:
        classifier = GridSearchCV(model, paramter_combinations[i])
    else:
        classifier = model

    print('Training ', model.__class__.__name__, '...')
    classifier.fit(train_features, train_labels)
    print('Training finished...')

    print('Predicting with ', model.__class__.__name__, '...')
    predictions = classifier.predict(test_features)
    print('Predictiion finished...')

    accuracy = calculate_accuracy(predictions, test_labels)
    accuracy_train = calculate_accuracy(predictions, train_labels)
    print(model.__class__.__name__, ' accuracy: ', accuracy)
    print(model.__class__.__name__, ' accuracy_train: ', accuracy_train)
    print('='*30)

    if hasattr(classifier, 'best_params_'):
        save_classifier(model.__class__.__name__, accuracy, classifier.best_params_)
    else:
        save_classifier(model.__class__.__name__, accuracy)
