import sys
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

import encode
from config import config

def file_exists(file_path):
    if not file_path:
        return False
    else:
        return os.path.isfile(file_path)

read_file = sys.argv[1]
vectorizer__save_file = sys.argv[2]

features_field = 'question'
label_field = 'questionType'

if len(sys.argv) > 2:
    vectorizer__save_file = sys.argv[2]

if len(sys.argv) > 4:
    features_field = sys.argv[3]
    label_field = sys.argv[4]

parsed_data = encode.parse_from_json(read_file, features_field, label_field)

vectorizer = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 2))

if file_exists(vectorizer__save_file):
    vectorizer = vectorizer__save_file


vectorizer = encode.load_or_train_vectorizer(
    vectorizer=vectorizer,
    train_features=parsed_data['features'],
    save_file_name=vectorizer__save_file)

features, labels = encode.transform_data(
    parsed_data,
    vectorizer)

for i, model in enumerate(config['models']):
    print('='*30)

    paramter_combinations = config['models_parameters']
    if len(paramter_combinations) > i:
        classifier = GridSearchCV(model, paramter_combinations[i])
    else:
        classifier = model

    scores = cross_val_score(classifier,features, labels, cv=5)
    mean_accuracy = scores.mean()

    print('='*30)
    print(model.__class__.__name__)
    print('mean accuracy: ', mean_accuracy)
    print('=' * 30)

    if hasattr(classifier, 'best_params_'):
        encode.save_classifier(
            classifier,
            model.__class__.__name__,
            mean_accuracy,
            classifier.best_params,
            'yes_no')
    else:
        encode.save_classifier(
            classifier,
            model.__class__.__name__,
            mean_accuracy,
            'yes_no')