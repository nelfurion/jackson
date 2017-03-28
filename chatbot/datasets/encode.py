import nltk
import string
import ast

from sklearn.externals import joblib

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from sklearn.feature_extraction.text import TfidfVectorizer

VECTORIZERS_FOLDER = '../models/vectorizers/'
CLASSIFIERS_FOLDER = '../models/classifiers/'
PUNCTUATIONS = string.punctuation + '?\n'

def encode_data(parsed_data):
    '''
    parsed_data: dictionary with 'features', 'labels', 'sublabels'
    '''

    pos_tag_strings = get_pos_tags(parsed_data['features'])

    for i in range(len(parsed_data['features'])):
        parsed_data['features'][i] += ' ' + pos_tag_strings[i]

    return parsed_data

def tokenize(sentences_array):
    return [nltk.word_tokenize(sentence) for sentence in sentences_array]

def transform_data(encoded_data, vectorizer):
    features = encoded_data['features']
    features = vectorizer.transform(features).toarray()

    return (features, encoded_data['labels'])

def load_or_train_vectorizer(vectorizer = None, train_features = None, save_file_name = None):
    if type(vectorizer) is str:
        return joblib.load(VECTORIZERS_FOLDER + vectorizer)

    if save_file_name is None:
        raise ValueError('If training a vectorizer, save_file_name cannot be None.')

    return train_vectorizer(vectorizer, train_features, save_file_name)

def train_vectorizer(vectorizer, train_features, file_name):
    if vectorizer is None:
        vectorizer = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 3))

    vectorizer.fit(train_features)

    file_name = VECTORIZERS_FOLDER + file_name + '.pkl'
    joblib.dump(vectorizer, file_name)

    return vectorizer

def get_pos_tags(questions):
    tokenized_questions = tokenize(questions)
    tagged_questions = [nltk.pos_tag(question) for question in tokenized_questions]
    pos_tag_strings = []
    for i in range(len(tagged_questions)):
        question_tags = [pos for word, pos in tagged_questions[i]]
        pos_tag_strings.append(' '.join(question_tags))

    return pos_tag_strings

def parse_data(file, stemmer=SnowballStemmer("english")):
    features = []
    labels = []

    with open(file) as f:
        content = f.readlines()[1:]
        for line in content:
            parts = line.split(' ', 1)
            question = parts[1]
            question_types = parts[0].split(':')
            main_type = question_types[0]

            words = [word for word in question.split(' ')
                        if word not in stopwords.words('english') and
                        word not in PUNCTUATIONS]

            for i in range(len(words)):
                words[i] = stemmer.stem(words[i])

            question = ' '.join(words)

            labels.append(main_type)
            features.append(question)

    parsed_data = {
        'features': features,
        'labels': labels
    }

    return parsed_data

def save_classifier(classifier, classifier_name, accuracy, parameters = None, folder=''):
    file_name = 'q_clf_' + classifier_name + '_'
    if parameters:
        for key, value in parameters.items():
            file_name += str(key) + '='
            file_name += str(value) + '_'

    file_name += 'accuracy=' + str(accuracy)
    file_name += '.pkl'

    if len(folder) > 0 and folder[len(folder) - 1] != '/':
        folder += '/'

    print('NAME:')
    print(file_name)

    joblib.dump(classifier, CLASSIFIERS_FOLDER + folder + file_name)