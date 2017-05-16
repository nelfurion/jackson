import json

from urllib.request import urlopen
from .service import Service
from .config import config

class TopicClassificationService(Service):
    """Microservice for topic classification."""

    def get_topic(self, question):
        params = {
            "question": question
        }

        request_url = self._create_request(params, config['topic_classification_url'])

        response = urlopen(request_url).read()
        response = response.decode('utf-8')
        response = json.loads(response)

        return response
