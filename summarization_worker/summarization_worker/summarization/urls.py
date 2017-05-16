from django.conf.urls import url
from .controllers import summarization_controller

app_name = 'JacksonWebApp'

urlpatterns = [
    url(r'^summarize/$', summarization_controller.summarize, name='summarize'),
    url(r'^summary/$', summarization_controller.get_summary, name='get_summary'),
]