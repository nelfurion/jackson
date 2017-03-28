import timeit


import numpy

from config import config

import encode

from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.metrics import classification_report

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

print('Start loading data')
start = timeit.default_timer()
encoded_train_data = None
encoded_test_data = None

try:
    encoded_train_data = joblib.load('encoded_train_data.pkl')
    encoded_test_data = joblib.load('encoded_test_data.pkl')
except :
    encoded_train_data = encode.encode_data(encode.parse_data('./questions_train.txt'))
    encoded_test_data = encode.encode_data(encode.parse_data('./questions_test.txt'))

    joblib.dump(encoded_train_data, 'encoded_train_data.pkl')
    joblib.dump(encoded_test_data, 'encoded_test_data.pkl')


vectorizer = encode.load_or_train_vectorizer(
    vectorizer='Vectorizerngram_range=1,3;analyzer=word.pkl',
    train_features=encoded_train_data['features'])

train_features, train_labels = encode.transform_data(encoded_train_data, vectorizer)
test_features, test_labels = encode.transform_data(encoded_test_data, vectorizer)

stop = timeit.default_timer()

print('Finish loading data')
print('Time: ', stop - start)

print('Start training')
start = timeit.default_timer()

for i, model in enumerate(config['models']):
    print('='*30)

    parameter_combinations = config['models_parameters']
    if len(parameter_combinations) > i:
        classifier = GridSearchCV(model, parameter_combinations[i], verbose=True)
    else:
        classifier = model

    print('Training ', model.__class__.__name__, '...')
    classifier.fit(train_features, train_labels)
    print('Training finished...')

    print('Predicting with ', model.__class__.__name__, '...')
    predictions = classifier.predict(test_features)
    print('Test prediction finished...')
    train_set_predictions = classifier.predict(train_features)
    print('Predictiion finished...')

    accuracy = calculate_accuracy(predictions, test_labels)

    accuracy_train = calculate_accuracy(train_set_predictions, train_labels)

    report = get_report(
        model.__class__.__name__,
        test_labels, predictions,
        train_labels,
        train_set_predictions)

    print(report)

    with open('report-2.txt', 'a') as report_file:
        report_file.write(report)

    if hasattr(classifier, 'best_params_'):
        encode.save_classifier(classifier, model.__class__.__name__, accuracy, classifier.best_params_)
    else:
        encode.save_classifier(classifier, model.__class__.__name__, accuracy)


stop = timeit.default_timer()

print('Finish training')
print('Time: ', stop - start)