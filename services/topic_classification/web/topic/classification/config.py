import os

current_path = os.path.dirname(os.path.abspath(__file__))

config = {
    'question_classifier': current_path + '/../models/classifiers/q_clf_RandomForestClassifier_n_estimators=200_accuracy=0.7895791583166333.pkl',
    'vectorizer': current_path + '/../models/vectorizers/Vectorizerngram_range=1,3;analyzer=word.pkl'
}
