import math
import multiprocessing
import time

from requests_futures.sessions import FuturesSession
from rq import Queue

import worker
from .preprocess.tokenizer import Tokenizer
from .config import config
from .parser import Parser
from .phrase_extractor import PhraseExtractor
from .preprocess.lemmatizer import Lemmatizer
from .sentence_scorer import SentenceScorer

SENTENCES_PER_REQUEST = 10
sentences_scores = []

def summarize_by_input_frequency(sentence_count, articles, nj_phrases):
    queue = Queue(connection = worker.conn)

    job = queue.enqueue(start_summarization_jobs,sentence_count,articles,nj_phrases)

    return job.get_id()

def append_result(session, response):
    try:
        data = response.json()
        sentence_scores = data['sentence_scores']

        if len(sentence_scores) > 0:
            sentences_scores.extend(sentence_scores)
    except:
        print('---------------Erorr occured in summarization...----------------')


def start_summarization_jobs(sentence_count, articles, nj_phrases):
    sentence_scorer = SentenceScorer(
        lemmatizer = Lemmatizer(),
        tokenizer = Tokenizer(),
        parser = Parser.get_instance(),
        phrase_extractor = PhraseExtractor())

    result_lock = multiprocessing.Lock()
    endpoint_index = 0
    endpoints = config['summarization_endpoints']
    endpoints_count = len(endpoints)

    tokenizer = Tokenizer()

    body = {
        'noun_phrases': list(nj_phrases['noun_phrases']),
        'adjective_phrases': list(nj_phrases['adjective_phrases']),
        'nouns': list(nj_phrases['nouns']),
        'adjectives': list(nj_phrases['adjectives'])
    }

    max_workers_count = len(articles) * SENTENCES_PER_REQUEST
    request_session = FuturesSession(max_workers=max_workers_count)
    requests = []
    for article in articles:
        page_sentences = tokenizer.tokenize_sentences(article['text'])
        body['title'] = article['title']

        page_sentences_count = len(page_sentences)
        parts_count =  int(math.ceil(page_sentences_count / SENTENCES_PER_REQUEST))

        for i in range(parts_count):
            endpoint = endpoints[endpoint_index]
            begin_index = math.ceil(i * page_sentences_count / parts_count)
            end_index = math.ceil((i + 1) * page_sentences_count / parts_count)

            body['text'] = ' '.join(page_sentences[begin_index: end_index])
            page_part_request = request_session.post(
                endpoint,
                json=body,
                background_callback=append_result,
                timeout=30)

            requests.append(page_part_request)

            endpoint_index += 1

            if endpoint_index >= endpoints_count:
                endpoint_index = 0

    for request in requests:
        result_lock.acquire()

        try:
            request.result()

        except:
            print('-------Error: Connection closed...-------')

        result_lock.release()

    best_sentences = sentence_scorer.get_best_unique_sentences(sentences_scores, sentence_count)

    return best_sentences