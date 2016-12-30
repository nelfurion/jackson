from django.conf.urls import url
from . import views

app_name = 'chatbot'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^chat/$', views.ChatView.as_view(), name='chat_view'),
]