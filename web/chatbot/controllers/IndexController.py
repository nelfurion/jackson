from django.shortcuts import render
from django.views import View

def handle(request):
    statistics = {
        'chats_count': 1350,
        'chat_logs_count': 346
    }

    return render(request, 'chatbot/index.html', {'statistics': statistics})