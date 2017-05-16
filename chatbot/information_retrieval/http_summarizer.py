import multiprocessing
import math
import time

from preprocess.tokenizer import Tokenizer

from requests_futures.sessions import FuturesSession

from.summarizer import Summarizer
from .config import config

SENTENCES_PER_REQUEST = 10

class HttpSummarizer(Summarizer):
    def __init__(self, lemmatizer, tokenizer, sentence_scorer, summarization_service, min_freq=0.1, max_freq=0.9):
        super().__init__(lemmatizer, tokenizer, sentence_scorer, min_freq, max_freq)

        self.summarization_service = summarization_service
        self.sentence_scorer = sentence_scorer
        self.result_lock = multiprocessing.Lock()
        self.remaining_articles = 0

        self.endpoints = config['summarization_endpoints']
        self.sentences_scores = []

    def summarize_by_input_frequency(self, sentence_count, articles, nj_phrases):
        start = time.time()
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

        self.request_session = FuturesSession(max_workers=max_workers_count)

        end = time.time()
        print('SUMMARIZTION TIME BEFORE SENDING REQS: ', end - start)
        start = time.time()
        requests = []
        for article in articles:
            page_sentences = tokenizer.tokenize_sentences(article['text'])
            body['title'] = article['title']

            page_sentences_count = len(page_sentences)
            parts_count =  int(math.ceil(page_sentences_count / SENTENCES_PER_REQUEST))

            for i in range(parts_count):
                endpoint = endpoints[endpoint_index]
                #print('Creating request to: ', endpoint)
                begin_index = math.ceil(i * page_sentences_count / parts_count)
                end_index = math.ceil((i + 1) * page_sentences_count / parts_count)

                body['text'] = ' '.join(page_sentences[begin_index: end_index])
                page_part_request = self.request_session.post(
                    endpoint,
                    json=body,
                    background_callback=self.append_result)

                requests.append(page_part_request)

                endpoint_index += 1

                if endpoint_index >= endpoints_count:
                    endpoint_index = 0

        end = time.time()
        print('REQUESTS SENT TIME: ', end - start)
        start = time.time()
        for request in requests:
            try:
                request.result()
            except:
                print('-------Error: Connection closed...-------')
        end = time.time()
        print('REQUESTS FINISHED TIME: ', end - start)

        start = time.time()
        best_sentences = self.sentence_scorer.get_best_unique_sentences(self.sentences_scores, sentence_count)
        end = time.time()

        print('SCORING TIME: ', end - start)
        return best_sentences

    def append_result(self, session, response):
        #print("Got response from summarization...")

        try:
            data = response.json()
            sentence_scores = data['sentence_scores']

            if len(sentence_scores) > 0:
                self.result_lock.acquire()
                self.sentences_scores.extend(sentence_scores)
                self.result_lock.release()
        except:
            print('---------------Erorr occured in summarization...----------------')