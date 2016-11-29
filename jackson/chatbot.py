import numpy

from information_retrieval.nltk_entity_extractor import NltkEntityExtractor

class Chatbot:
    def __init__(self, text_processor, question_classifier, data_service, summarizer):
        self.text_processor = text_processor
        self.context = ""
        self.last_utterance = ""
        self.question_classifier = question_classifier
        self.data_service = data_service
        self.summarizer = summarizer
        self.entity_extractor = NltkEntityExtractor()

    def read(self, utterance):
        text = self.text_processor.process(utterance)
        self.context += (utterance)
        self.last_utterance = utterance

    def answer(self):
        features = self.text_processor.vectorize(self.last_utterance)
        topic = self.question_classifier.predict(features)
        print('[', topic, ']')

        #if topic is HUM
        entities_info = []

        entities = self.entity_extractor.get_entities(self.last_utterance)
        for entity in entities:
            entity_info = self.data_service.find(entity)
            summary = self.summarizer.summarize(3, entity_info)
            entities_info.append(entity + '\n' + summary)

        final_answer = '\n'.join(entities_info)

        return final_answer
