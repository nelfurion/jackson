import timeit


import numpy

from config import config

import encode

from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.metrics import classification_report

def get_report(model_name, test_labels, test_predictions, train_labels, train_predictions):
    accuracy = calculate_accuracy(test_predictions, test_labels)
    accuracy_train = calculate_accuracy(train_predictions, train_labels)

    report = '=' * 30 + '\n'

    report += '{} accuracy: {}'.format(model_name, accuracy)
    report += '{} accuracy_train: {}'.format(model_name, accuracy_train)

    report += 'Detailed classification report:\n'
    report += 'The model is trained on the full development set.\n'
    report += 'The scores are computed on the full evaluation set.\n'

    report += classification_report(test_labels, test_predictions)

    report += '\n' + '=' * 30 + '\n'

    return report

def calculate_accuracy(predictions, test_labels):
    correct_count = 0
    for i in range(len(predictions)):
        if predictions[i] == test_labels[i]:
            correct_count += 1

    return correct_count / len(predictions)

encoded_train_data = joblib.load('encoded_train_data.pkl')
encoded_test_data = joblib.load('encoded_test_data.pkl')

vectorizer = encode.load_or_train_vectorizer(
    vectorizer='Vectorizerngram_range=1,3;analyzer=word.pkl')

train_features, train_labels = encode.transform_data(encoded_train_data, vectorizer)
test_features, test_labels = encode.transform_data(encoded_test_data, vectorizer)


classifier = joblib.load('../models/classifiers/q_clf_RandomForestClassifier_n_estimators=200_accuracy=0.7895791583166333.pkl')
predictions = classifier.predict(test_features)
train_set_predictions = classifier.predict(train_features)
accuracy = calculate_accuracy(predictions, test_labels)

report = get_report(
    classifier.__class__.__name__,
        test_labels, predictions,
        train_labels,
        train_set_predictions)

print(report)

