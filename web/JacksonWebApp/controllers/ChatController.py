import json

from django.http import JsonResponse
from django.shortcuts import render

import os
import sys
sys.path.append(os.getcwd())
print(os.getcwd())

import timeit

from jackson import get_chatbot

def handle(request):
    if(request.method == 'POST'):
        body_data = json.loads(request.body.decode(encoding='UTF-8'))
        user_input = body_data['user_input']

        before = timeit.default_timer()
        jackson = get_chatbot()
        answer = jackson.read_and_answer(user_input)
        after = timeit.default_timer()

        print('Time taken: ', after - before)

        return JsonResponse({
            'answer': answer
        })
    else:
        return render(request, 'JacksonWebApp/chat.html')