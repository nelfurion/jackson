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

vectorizer = joblib.load('../models/vectorizers/TfidfVectorizer.pkl')

train_features, train_labels, train_sublabels = encode.encode_data(
    './questions_train.txt',
    vectorizer)


test_features, test_labels, test_sublabels = encode.encode_data(
    './questions_test.txt',
    vectorizer)

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
    print(model.__class__.__name__, ' accuracy: ', accuracy)
    print('='*30)

    if hasattr(classifier, 'best_params_'):
        save_classifier(model.__class__.__name__, accuracy, classifier.best_params_)
    else:
        save_classifier(model.__class__.__name__, accuracy)
