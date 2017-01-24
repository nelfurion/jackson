from sklearn.externals import joblib

from information_retrieval.summarizer import Summarizer
from information_retrieval.parser import Parser

from services.wikipedia_service import WikipediaService
from services.database_service import DatabaseService

from preprocess.tokenizer import Tokenizer
from preprocess.stemmer import Stemmer
from preprocess.lemmatizer import Lemmatizer

from chatbot.text_processor import TextProcessor
from chatbot.chatbot import Chatbot
from chatbot.config import config
from chatbot.data_manager import  DataManager

text_processor = TextProcessor(
    Tokenizer(),
    Stemmer(),
    joblib.load(config['vectorizer']),
    Lemmatizer())

jackson = Chatbot(
    text_processor,
    joblib.load(config['question_classifier']),
    WikipediaService(),
    DataManager(
        text_processor,
        DatabaseService(),
        WikipediaService(),
        None,
        Parser.get_instance()),
    Summarizer(
        Lemmatizer()
    ))