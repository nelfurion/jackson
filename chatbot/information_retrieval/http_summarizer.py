import json
import requests

from .summarizer import Summarizer
from .config import config

class HttpSummarizer(Summarizer):
    def __init__(self, lemmatizer, tokenizer, sentence_scorer, summarization_service, min_freq=0.1, max_freq=0.9):
        super().__init__(lemmatizer, tokenizer, sentence_scorer, min_freq, max_freq)

        self.summarization_service = summarization_service
        self.sentence_scorer = sentence_scorer
        self.remaining_articles = 0

        self.endpoints = config['summarization_endpoints']

    def summarize_by_input_frequency(self, sentence_count, articles, nj_phrases):
        body = {
            'noun_phrases': list(nj_phrases['noun_phrases']),
            'adjective_phrases': list(nj_phrases['adjective_phrases']),
            'nouns': list(nj_phrases['nouns']),
            'adjectives': list(nj_phrases['adjectives']),
            'articles': articles,
            'sentence_count': sentence_count
        }

        url = config['summarization_worker_endpoint']
        job_url = config['summarization_job_endpoint']

        summarization_job_request = requests.post(
            url,
            json=body)

        json_response = json.loads(summarization_job_request.text)
        jobId = json_response['jobId']

        return (jobId, job_url)