import json
import timeit

from django.http import JsonResponse
from django.shortcuts import render

from rq.job import Job

import os
import sys
sys.path.append(os.getcwd())
print(os.getcwd())

import worker
from jackson import get_chatbot

def handle(request):
    if(request.method == 'POST'):
        start = timeit.default_timer()
        jackson = get_chatbot() 
        body_data = json.loads(request.body.decode(encoding='UTF-8'))
        user_input = body_data['user_input']

        print('received request')

        answer = jackson.read_and_answer(user_input)

        end = timeit.default_timer()
        print('Time taken: ', end - start)
        if isinstance(answer, tuple):
            return JsonResponse({
                'answer': answer[0],
                'id': True,
                'endpoint': answer[1]
            })
        else:
            return JsonResponse({
                'answer': answer,
                'id': False
            })
    else:
        return render(request, 'JacksonWebApp/chat.html')

def get_job_result(request):
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