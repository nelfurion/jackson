'''
TODO:
There are a number of wrong thing in this file...
'''
import numpy

from encode import encode_data
from encode import parse_data

#Importing classifiers
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib

def calculate_accuracy(predictions, test_labels):
    correct_count = 0
    for i in range(len(predictions)):
        if predictions[i] == test_labels[i]:
            correct_count += 1

    return correct_count / len(predictions)

def save_classifier(classifier_name, parameters, accuracy):
    file_name = 'q_clf_' + classifier_name + '_'
    for key, value in parameters.items():
        file_name += str(key) + '='
        file_name += str(value) + '_'

    file_name += 'accuracy=' + str(accuracy)
    file_name += '.pkl'

    joblib.dump(classifier, '../models/classifiers/' + file_name)

train_features, \
train_labels, \
train_sublabels, \
test_features, \
test_labels, \
test_sublabels = encode_data('./questions_train.txt', './questions_test.txt')

models = [
    MultinomialNB()
]

parameters = [{
        'alpha': numpy.arange(0, 1.1, 0.1)
}]

for i, model in enumerate(models):
    print('='*30)
    classifier = GridSearchCV(model, parameters[i])
    print('Training ', model.__class__.__name__, '...')
    classifier.fit(train_features, train_labels)
    print('Training finished...')

    print('Predicting with ', model.__class__.__name__, '...')
    predictions = classifier.predict(test_features)
    print('Predictiion finished...')

    accuracy = calculate_accuracy(predictions, test_labels)
    print(model.__class__.__name__, ' accuracy: ', accuracy)
    print('='*30)

    save_classifier(model.__class__.__name__, classifier.best_params_, accuracy)
