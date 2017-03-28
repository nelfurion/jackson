from sklearn.externals import joblib

from information_retrieval.summarizer import Summarizer
from information_retrieval.multiprocess_summarizer import MultiProcessSummarizer
from information_retrieval.parser import Parser
from information_retrieval.svo_extractor import SvoExtractor
from information_retrieval.phrase_extractor import PhraseExtractor
from information_retrieval.nltk_entity_extractor import NltkEntityExtractor
from information_retrieval.summarization_task import SummarizationTask
from information_retrieval.sentence_scorer import SentenceScorer

from utils.consumer import Consumer

from services.wikipedia_service import WikipediaService
from services.neo4j_service import Neo4jService

from preprocess.tokenizer import Tokenizer
from preprocess.stemmer import Stemmer
from preprocess.lemmatizer import Lemmatizer

from chatbot.text_processor import TextProcessor
from chatbot.chatbot import Chatbot
from chatbot.config import config
from chatbot.data_manager import  DataManager

tokenizer = Tokenizer()
wikipedia_service = WikipediaService()
neo4j_service = Neo4jService()
nltk_entity_extractor = NltkEntityExtractor(tokenizer)

def get_chatbot():
    #lemmatizer is not thread safe
    lemmatizer = Lemmatizer()

    text_processor = TextProcessor(
        tokenizer,
        Stemmer(),
        joblib.load(config['vectorizer']),
        lemmatizer)

    svo_extractor = SvoExtractor(text_processor, PhraseExtractor())
    sentence_scorer = SentenceScorer(
        lemmatizer,
        tokenizer,
        Parser.get_instance(),
        PhraseExtractor())

    '''
    summarizer = Summarizer(
        lemmatizer,
        tokenizer,
        sentence_scorer
    )
    '''

    summarizer = MultiProcessSummarizer(
        lemmatizer,
        tokenizer,
        sentence_scorer,
        SummarizationTask,
        Consumer)


    data_manager = DataManager(
        text_processor,
        neo4j_service,
        wikipedia_service,
        Parser.get_instance(),
        svo_extractor,
        summarizer)

    chatbot = Chatbot(
        text_processor,
        joblib.load(config['question_classifier']),
        data_manager,
        nltk_entity_extractor)

    return chatbot

if __name__ == '__main__':
    jackson = get_chatbot()
    while True:
        user_input = input('Say something: ')
        answer = jackson.read_and_answer(user_input)
        print('Jackson: ', answer)
