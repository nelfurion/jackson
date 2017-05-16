import os

current_path = os.path.dirname(os.path.abspath(__file__))

config = {
    'question_classifier': current_path + '/../models/classifiers/q_clf_RandomForestClassifier_n_estimators=200_accuracy=0.7895791583166333.pkl',
    'vectorizer': current_path + '/../models/vectorizers/Vectorizerngram_range=1,3;analyzer=word.pkl',
    'titles_per_phrase_human': 1,
    'titles_per_phrase_other': 2,
    'response_empty_string': 'You sent an empty string.',
    'response_default': 'I don\'t know. What do you think?',
    'response_not_learned': 'Right back at you.',
    'response_learned': 'I learned that {info}'
}
