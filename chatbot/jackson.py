from sklearn.externals import joblib

from information_retrieval.config import config
from information_retrieval.entity_extractor import EntityExtractor
from information_retrieval.parser import Parser
from information_retrieval.phrase_extractor import PhraseExtractor
from information_retrieval.sentence_scorer import SentenceScorer
from information_retrieval.http_summarizer import HttpSummarizer
from information_retrieval.multiprocess_summarizer import MultiProcessSummarizer
from information_retrieval.summarization_task import SummarizationTask
from information_retrieval.topic_classifier import TopicClassifier
from information_retrieval.svo_extractor import SvoExtractor
from information_retrieval.topic_classifier_local import TopicClassifierLocal

from utils.consumer import Consumer

from services.topic_classification import TopicClassificationService
from services.summarization_service import SummarizationService

from chatbot.chatbot import Chatbot
from information_retrieval.config import config
from chatbot.data_manager import DataManager

from preprocess.lemmatizer import Lemmatizer
from preprocess.stemmer import Stemmer
from preprocess.tagged_words_corpus import TaggedWordsCorpus
from preprocess.text_processor import TextProcessor
from preprocess.tokenizer import Tokenizer

from services.neo4j_service import Neo4jService
from services.wikipedia_service import WikipediaService

tokenizer = Tokenizer()
stemmer = Stemmer()
wikipedia_service = WikipediaService()
neo4j_service = Neo4jService()

# topic_classifier = TopicClassifier(TopicClassificationService())
summarization_service = SummarizationService()

tagged_words_corpus = TaggedWordsCorpus()

parser = Parser.get_instance()

def get_chatbot():
    lemmatizer = Lemmatizer()

    text_processor = TextProcessor(
        tokenizer,
        stemmer,
        joblib.load(config['vectorizer']),
        lemmatizer,
        Parser.get_instance(),
        tagged_words_corpus)

    phrase_extractor = PhraseExtractor(text_processor)
    svo_extractor = SvoExtractor(text_processor, phrase_extractor)
    sentence_scorer = SentenceScorer(text_processor, phrase_extractor)
    entity_extractor = EntityExtractor(text_processor)
    topic_classifier = TopicClassifierLocal(text_processor)

    '''
    summarizer = Summarizer(
        text_processor,
        sentence_scorer
    )
    '''

    '''
    summarizer = HttpSummarizer(
        text_processor,
        sentence_scorer,
        summarization_service)
    '''

    summarizer = MultiProcessSummarizer(
        text_processor,
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
        topic_classifier,
        data_manager,
        entity_extractor)

    return chatbot

if __name__ == '__main__':
    jackson = get_chatbot()
    while True:
        user_input = input('Say something: ')
        answer = jackson.read_and_answer(user_input)
        print('Jackson: ', answer)
