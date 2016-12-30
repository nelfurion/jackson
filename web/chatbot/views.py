import json
import sys
sys.path.append('../')

from jackson import jackson

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

def index(request):
    statistics = {
        'chats_count': 1350,
        'chat_logs_count': 346
    }

    return render(request, 'chatbot/index.html', {'statistics': statistics})

class ChatView(View):
    def get(self, request):
        return render(request, 'chatbot/chat.html')

    def post(self, request):
        body_data = json.loads(request.body.decode(encoding='UTF-8'))
        user_input = body_data['user_input']
        jackson.jackson.read(user_input)
        return JsonResponse({
            'answer': jackson.jackson.answer()
        })

class LogsView(View):
    def get(self, request):
        return render(request, 'chatbot/logs.html')