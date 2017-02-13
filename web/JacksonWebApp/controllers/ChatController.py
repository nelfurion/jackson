import json

from django.http import JsonResponse
from django.shortcuts import render

import os
import sys
sys.path.append(os.getcwd())
print(os.getcwd())

from jackson import jackson

def handle(request):
    if(request.method == 'POST'):
        body_data = json.loads(request.body.decode(encoding='UTF-8'))
        user_input = body_data['user_input']

        answer = jackson.read_and_answer(user_input)

        return JsonResponse({
            'answer': answer
        })
    else:
        return render(request, 'JacksonWebApp/chat.html')