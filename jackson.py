from sklearn.externals import joblib

from chatbot import Chatbot
from text_processor import TextProcessor
from snowball_stemmer import SnowballStemmer
from whitespace_tokenizer import WhiteSpaceTokenizer

from config import config

text_processor = TextProcessor(
    WhiteSpaceTokenizer(), SnowballStemmer(),
    joblib.load(config['vectorizer']))

jackson = Chatbot(
    text_processor,
    joblib.load(config['question_classifier']))

while True:
    user_input = input()
    jackson.read(user_input)
    print(jackson.answer())
