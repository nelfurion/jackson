from django.conf.urls import url

from .controllers import topic_controller

urlpatterns = [
    url(r'^$', topic_controller.get_topic, name='get_topic'),
]
