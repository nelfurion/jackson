import math
import multiprocessing
import time
import json
import requests

from requests_futures.sessions import FuturesSession
from rq import Queue as RqQueue

from queue import *

import worker
from .preprocess.tokenizer import Tokenizer
from .config import config
from .parser import Parser
from .phrase_extractor import PhraseExtractor
from .preprocess.lemmatizer import Lemmatizer
from .sentence_scorer import SentenceScorer

SENTENCES_PER_REQUEST = 10
sentences_scores = []
request_session = None

def summarize_by_input_frequency(sentence_count, articles, nj_phrases):
    queue = RqQueue(connection = worker.conn)

    job = queue.enqueue(start_summarization_jobs,sentence_count,articles,nj_phrases)

    return job.get_id()

def append_result(session, response):
    try:
        data = response.json()
        sentence_scores = data['sentence_scores']

        if len(sentence_scores) > 0:
            sentences_scores.extend(sentence_scores)
    except:
        print('Error: Could not retrieve json from score result...')

def start_summarization_jobs(sentence_count, articles, nj_phrases):
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
    sent_requests = Queue()

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
                background_callback=append_result)

            sent_requests.put({
                'future': page_part_request,
                'endpoint': endpoint,
                'body': body,
                'callback': append_result
            })

            endpoint_index += 1

            if endpoint_index >= endpoints_count:
                endpoint_index = 0

    save_results(request_session, result_lock, sent_requests)

    return get_best_sentences(sentence_count)

def get_best_sentences(sentence_count):
    sentence_scorer = SentenceScorer(
        lemmatizer=Lemmatizer(),
        tokenizer=Tokenizer(),
        parser=Parser.get_instance(),
        phrase_extractor=PhraseExtractor())

    best_sentences = sentence_scorer.get_best_unique_sentences(sentences_scores, sentence_count)

    return best_sentences

def save_results(session, result_lock, sent_requests):
    while(not sent_requests.empty()):
        request = sent_requests.get()
        result_lock.acquire()
        request_future = request['future']
        request_body = request['body']
        request_endpoint = request['endpoint']
        request_callback = request['callback']

        try:
            result = request_future.result()
            if ('DOCTYPE' in result.text) or (result.status_code >= 400):
                add_request_to_queue(session, sent_requests, request_endpoint, request_body, request_callback)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            print_error('Timeout error')
            add_request_to_queue(session, sent_requests, request_endpoint, request_body, request_callback)
        except Exception as e:
            print_error('Unexpected error')
            add_request_to_queue(session, sent_requests, request_endpoint, request_body, request_callback)

        result_lock.release()

    print('RESULTS SAVED')

def print_error(error):
    error_format = 'Error: {error}...'
    error_message = error_format.format(error=error)
    print(error_message)
    print('Readding request to queue...')


def add_request_to_queue(session, queue, endpoint, body, callback):
    request = session.post(
        endpoint,
        json=body,
        background_callback=callback)

    queue.put({
        'future': request,
        'endpoint': endpoint,
        'body': body,
        'callback': callback
    })
