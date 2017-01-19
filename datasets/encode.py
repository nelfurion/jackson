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

    first_words = [sentence.split()[0] for sentence in parsed_data['features']]

    features_tuple = get_pos_tags(parsed_data['features'])
    parsed_data['features'] = features_tuple[1]


    for i in range(len(parsed_data['features'])):
        parsed_data['features'][i] = 'a world'

    '''
    tokenized_questions = [nltk.word_tokenize(question) for question in parsed_data['features']]
    tagged_questions = [nltk.pos_tag(question) for question in tokenized_questions]
    ne_chunks = nltk.ne_chunk_sents(tagged_questions, binary=True)

    nodes = []
    for tree in ne_chunks:
        question_nes = []
        for child in tree:
            if hasattr(child, 'label') and child.label:
                question_nes.append(child.label())
                if child.label() != 'NE':
                    print(child.label())

        nodes.append(question_nes)

    for i in range(len(features_with_pos_tags)):
        features_with_pos_tags[i] += ' ' + first_words[i]
        if len(nodes[i]) > 0:
            features_with_pos_tags[i] += ' ' + ' '.join(nodes[i])
    '''

    return parsed_data

def tokenize(sentences_array):
    return [nltk.word_tokenize(sentence) for sentence in sentences_array]

def transform_data(encoded_data, vectorizer):
    features = encoded_data['features']
    features = vectorizer.transform(features).toarray()

    if 'sublabels' in encoded_data.keys():
        return (features, encoded_data['labels'], encoded_data['sublabels'])

    return (features, encoded_data['labels'])

def load_or_train_vectorizer(vectorizer = None, train_features = None, save_file_name = None):
    if type(vectorizer) is str:
        return joblib.load(vectorizer)

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
    pos_tags = []
    pos_tag_strings = []
    for i in range(len(tagged_questions)):
        question_tags = [pos for word, pos in tagged_questions[i]]
        pos_tags.append(question_tags)
        pos_tag_strings.append(' '.join(question_tags))

    return (pos_tags, pos_tag_strings)

def add_position_tags(questions):
    pos_tags = get_pos_tags(questions)[0]

    for i in range(len(questions)):
        questions[i] += ' '
        questions[i] += ' '.join(pos_tags[i])

    return questions

def parse_data(file, stemmer=SnowballStemmer("english")):
    features = []
    labels = []
    sublabels = []

    with open(file) as f:
        content = f.readlines()[1:]
        for line in content:
            parts = line.split(' ', 1)
            question = parts[1]
            question_types = parts[0].split(':')
            main_type = question_types[0]
            subtype = question_types[1]

            words = [word for word in question.split(' ')
                        if word not in stopwords.words('english') and
                        word not in PUNCTUATIONS]

            for i in range(len(words)):
                words[i] = stemmer.stem(words[i])

            question = ' '.join(words)

            labels.append(main_type)
            sublabels.append(subtype)
            features.append(question)

            parsed_data = {
                'features': features,
                'labels': labels,
                'sublabels': sublabels
            }

    return parsed_data

def parse_from_json(file_name, features_field, label_field):
    features = []
    labels = []
    with open(file_name, "r") as read_file:
        for line in read_file:
            obj = ast.literal_eval(line)

            features.append(obj[features_field])
            labels.append(obj[label_field])

    return {
        'features': features,
        'labels':labels
    }

def get_vectorizer_weights(vectorizer, features):
    weights = dict(zip(vectorizer.get_feature_names(), features.data))
    return weights

def print_to_file(text, action):
    with open("output.txt", action) as myfile:
        myfile.write(str(text))

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

    joblib.dump(classifier, CLASSIFIERS_FOLDER + folder + file_name)