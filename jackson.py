from sklearn.externals import joblib

from information_retrieval.summarizer import Summarizer
from information_retrieval.parser import Parser
from information_retrieval.svo_extractor import SvoExtractor
from information_retrieval.phrase_extractor import PhraseExtractor
from information_retrieval.nltk_entity_extractor import NltkEntityExtractor

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

svo_extractor = SvoExtractor(text_processor, PhraseExtractor())
summarizer = Summarizer(Lemmatizer())

data_manager = DataManager(
    text_processor,
    DatabaseService(),
    WikipediaService(),
    Parser.get_instance(),
    svo_extractor,
    summarizer)

jackson = Chatbot(
    text_processor,
    joblib.load(config['question_classifier']),
    data_manager,
    NltkEntityExtractor())