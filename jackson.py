from sklearn.externals import joblib

from information_retrieval.summarizer import Summarizer
from information_retrieval.parser import Parser

from services.wikipedia_service import WikipediaService
from services.database_service import DatabaseService

from preprocess.whitespace_tokenizer import WhiteSpaceTokenizer
from preprocess.snowball_stemmer import SnowballStemmer

from chatbot.text_processor import TextProcessor
from chatbot.chatbot import Chatbot
from chatbot.config import config
from chatbot.data_manager import  DataManager

text_processor = TextProcessor(
    WhiteSpaceTokenizer(),
    SnowballStemmer(),
    joblib.load(config['vectorizer']))

jackson = Chatbot(
    text_processor,
    joblib.load(config['question_classifier']),
    WikipediaService(),
    DataManager(DatabaseService(), WikipediaService(), None, Parser()),
    Summarizer())