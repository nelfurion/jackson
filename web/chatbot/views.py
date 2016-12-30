from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse
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
        return JsonResponse({'asd':'a'})