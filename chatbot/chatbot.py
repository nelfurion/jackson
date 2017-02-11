import string
import re

from .question_types import QuestionTypes

class Chatbot:
    def __init__(self, text_processor, question_classifier, data_service, data_manager, summarizer, entity_extractor):
        self.text_processor = text_processor
        self.log = ""
        self.last_utterance = ""
        self.tokenized_utterance = []
        self.question_classifier = question_classifier
        self.data_service = data_service
        self.data_manager = data_manager
        self.summarizer = summarizer
        self.entity_extractor = entity_extractor
        self.remembered = False
        self.last_question_type = None

    def read(self, utterance):
        self.last_question_type = self._get_question_type(utterance)
        self.log += (utterance)
        self.last_utterance = self._remove_punctuation(utterance)
        self.tokenized_utterance = self.text_processor.tokenize(self.last_utterance)

        print('Last question type: ', self.last_question_type)
        if self.last_question_type == QuestionTypes.Declarative:
            isRemembered = self.data_manager.try_remember(self.tokenized_utterance)
            self.remembered = isRemembered

    def answer(self):
        if (self.last_question_type == QuestionTypes.Declarative
            and self.remembered):
            return self._answer_declarative()
        elif self.last_question_type == QuestionTypes.Informative:
            return self._answer_informative()

    def _answer_informative(self):
        answer = self.data_manager.try_answer(self.tokenized_utterance) or ''
        topic = self._get_topic()
        print('TOPIC: ')
        print(topic)


        if topic in ['HUM', 'ABBR'] and not answer:
            entities = self._get_entities()
            answer = self.data_manager.answer_from_wiki(entities, topic)

        if topic in ['ENTY', 'DESC', 'NUM', 'LOC'] and not answer:
            phrases = self.data_manager.get_search_phrases(self.tokenized_utterance)
            answer = self.data_manager.answer_from_wiki(phrases, topic)

        if not answer or len(answer) == 0:
            answer = "I don't know. What do you think?"

        return answer

    def _answer_declarative(self):
        return 'I learned that ' + self.last_utterance

    def _get_topic(self):
        tagged_words = self.text_processor.get_pos_tags(self.tokenized_utterance)
        pos_tags = [pos for word, pos in tagged_words]

        features_string = self.tokenized_utterance[0] + ' ' + ' '.join(pos_tags)
        features = self.text_processor.vectorize(features_string)

        return self.question_classifier.predict(features)

    def _remove_punctuation(self, utterance):
        punctuation_exp = '[' + string.punctuation + ']'
        return re.sub(
            punctuation_exp,
            '',
            utterance)

    def _get_entities(self):
        punctuation_exp = '[' + string.punctuation + ']'
        re.sub(
            punctuation_exp,
            '',
            self.last_utterance)

        return self.entity_extractor.get_entities(self.last_utterance)

    def _get_question_type(self, utterance):
        # TODO: find a way to categorize whether the question is informative or interogative
        mark = utterance[len(utterance) - 1]
        if mark == '.':
            return QuestionTypes.Declarative
        elif mark == '?':
            return QuestionTypes.Informative
        elif mark == '!':
            return QuestionTypes.Exclamatory