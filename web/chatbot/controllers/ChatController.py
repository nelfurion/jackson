import json
import sys
sys.path.append('../')

from jackson.jackson import jackson
from jackson.dialogue_manager import DialogueManager

from django.http import JsonResponse
from django.shortcuts import render

def handle(request):
    if(request.method == 'POST'):
        body_data = json.loads(request.body.decode(encoding='UTF-8'))
        user_input = body_data['user_input']

        jackson.read(user_input)

        return JsonResponse({
            'answer': jackson.answer()
        })
    else:
        return render(request, 'chatbot/chat.html')