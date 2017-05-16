import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rq.job import Job

import worker
from summarization.summarization.http_summarizer import summarize_by_input_frequency

@csrf_exempt
def summarize(request):
    if(request.method == 'POST'):
        body_data = json.loads(request.body.decode(encoding='UTF-8'))
        articles = body_data['articles']
        sentence_count = int(body_data['sentence_count'])

        nj_phrases = {
            'noun_phrases': body_data['noun_phrases'],
            'adjective_phrases': body_data['adjective_phrases'],
            'nouns': body_data['nouns'],
            'adjectives': body_data['adjectives']
        }

        jobId = summarize_by_input_frequency(sentence_count, articles, nj_phrases)

        return JsonResponse({
            'jobId': jobId
        })

@csrf_exempt
def get_summary(request):
    id = request.GET.get('id', '')
    job = Job.fetch(id, connection=worker.conn)

    if job.is_finished:
        return JsonResponse({
            'answer': job.result,
            'id': False
        })

    else:
        return JsonResponse({
            'answer': "Job not finished.",
            'id': True
        })