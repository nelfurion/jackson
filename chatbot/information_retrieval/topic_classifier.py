class TopicClassifier(object):
    """Classifies question answer type - a.k.a. topic."""
    def __init__(self, topic_service):
        self.topic_service = topic_service

    def predict(self, question):
        return self.topic_service.get_topic(question)
