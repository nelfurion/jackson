import json

from urllib.request import urlopen
from .service import Service
from .config import config

class SummarizationService(Service):
    """Microservice for text summarization."""

    def summarize(self, text):
        params = {
            "text": text
        }

        request_url = self._create_request(params, config['summarization_service_url'])

        response = urlopen(request_url).read()
        response = response.decode('utf-8')
        response = json.loads(response)

        return response
