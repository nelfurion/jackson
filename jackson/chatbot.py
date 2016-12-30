import string
import re
import sys
sys.path.append('../')

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

        answer = ''

        entities = self.entity_extractor.get_entities(self.last_utterance)
        print('ENTITIES:')
        print(entities)

        if topic == 'HUM':
            entities_info = []

            for entity in entities:
                entity_info = self.data_service.find(entity)
                summary = self.summarizer.summarize(3, entity_info)
                entities_info.append(entity + '\n' + summary)

            answer = '\n'.join(entities_info)

        if topic == 'ABBR':
            answer = ''
            punctuation_exp = '[' + string.punctuation + ']'
            last_utterance = re.sub(
                punctuation_exp,
                '',
                self.last_utterance)

            print(last_utterance)

            entities = self.entity_extractor.get_entities(last_utterance)
            print(entities)

            if len(entities) > 0:
                entities_info = []
                for entity in entities:
                    entity_info = self.data_service.find(entity)
                    if len(entity_info) > 0:
                        summary = self.summarizer.summarize(3, entity_info)
                        entities_info.append(entity + '\n' + summary)

                answer = '\n'.join(entities_info)
            else:
                tokens = self.text_processor.tokenize(self.last_utterance)
                #for token in tokens:

        if len(answer) == 0:
            answer = "I don't know. What do you think?"

        return answer
