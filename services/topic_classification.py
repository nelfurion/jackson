import json

from urllib.request import urlopen
from .service import Service
from .config import config

class TopicClassificationService(Service):
    """Microservice for topic classification."""
    def __init__(self, url = config['topic_classification_url']):
        super().__init__()

    def get_topic(self, question):
        params = {
            "question": question
        }

        request_url = self._create_request(params)
