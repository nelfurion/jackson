import sys
sys.path.append('../')
sys.path.append('../preprocess')

from sklearn.externals import joblib
from clint.textui import colored

from information_retrieval.summarizer import Summarizer
from services.wikipedia_service import WikipediaService
from preprocess.whitespace_tokenizer import WhiteSpaceTokenizer
from preprocess.snowball_stemmer import SnowballStemmer
from .text_processor import TextProcessor
from .chatbot import Chatbot

from .config import config

text_processor = TextProcessor(
    WhiteSpaceTokenizer(),
    SnowballStemmer(),
    joblib.load(config['vectorizer']))

jackson = Chatbot(
    text_processor,
    joblib.load(config['question_classifier']),
    WikipediaService(),
    Summarizer())