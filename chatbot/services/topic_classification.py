from .service import Service
from .config import config

class TopicClassificationService(Service):
    """Microservice for topic classification."""

    def get_topic(self, question):
        arguments = {
            "question": question
        }

        endpoint = config['topic_classification_url']
        json_response = self.get(endpoint, arguments)

        return json_response
