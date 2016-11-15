import numpy

class Chatbot:
    def __init__(self, text_processor, question_classifier):
        self.text_processor = text_processor
        self.context = ""
        self.last_utterance = ""
        self.question_classifier = question_classifier

    def read(self, utterance):
        text = self.text_processor.process(utterance)
        self.context += (utterance)
        self.last_utterance = utterance

    def answer(self):
        features = self.text_processor.vectorize(self.last_utterance)
        topic = self.question_classifier.predict(features)

        return topic[0]
