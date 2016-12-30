import os

current_path = os.path.dirname(os.path.abspath(__file__))

config = {
    'question_classifier': current_path + '/../models/classifiers/q_clf_DecisionTreeClassifier_criterion=gini_class_weight=balanced_max_features=None_splitter=random_accuracy=0.7194388777555111.pkl',
    'vectorizer': current_path + '/../models/vectorizers/TfidfVectorizer_C.pkl'
}
