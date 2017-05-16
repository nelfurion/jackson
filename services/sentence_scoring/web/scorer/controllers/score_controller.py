import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..scoring.sentence_scorer import SentenceScorer
from ..scoring.lemmatizer import Lemmatizer
from ..scoring.parser import Parser
from ..scoring.phrase_extractor import PhraseExtractor
from ..scoring.tokenizer import Tokenizer

import time

lemmatizer = Lemmatizer()
tokenizer = Tokenizer()
parser = Parser.get_instance()
phrase_extractor = PhraseExtractor()

sentence_scorer = SentenceScorer(
            lemmatizer=Lemmatizer(),
            tokenizer=Tokenizer(),
            parser=Parser.get_instance(),
            phrase_extractor=PhraseExtractor())

@csrf_exempt
def handle(request):
    if(request.method == 'POST'):
        start = time.time()
        body_data = json.loads(request.body.decode(encoding='UTF-8'))
        text = body_data['text']
        title = body_data['title']

        print('BODY data')
        print(body_data)

        nj_phrases = {
            'noun_phrases': body_data['noun_phrases'],
            'adjective_phrases': body_data['adjective_phrases'],
            'nouns': body_data['nouns'],
            'adjectives': body_data['adjectives']
        }

        end = time.time()
        print('took request body', ' ', end - start)

        start = time.time()

        title_nj_phrases = sentence_scorer.get_title_phrases(title)
        title_score_and_matches = sentence_scorer.score_title(title_nj_phrases, nj_phrases)
        title_score = title_score_and_matches[0]

        end = time.time()
        print('title score: ', title_score, ' time: ', end - start)

        start = time.time()
        sentence_scores = sentence_scorer.score_sentences_by_input_phrases(text, title_score, nj_phrases)
        end = time.time()

        print('scored sentences', ' ', end - start)

        return JsonResponse({
            'sentence_scores': sentence_scores
        })