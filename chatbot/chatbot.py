import string
import re

from nltk.corpus import stopwords

from .question_types import QuestionTypes

class Chatbot:
    TITLES_PER_PHRASE = 2
    PUNCTUATIONS = string.punctuation + '?\n'

    def __init__(self, text_processor, question_classifier, data_manager, entity_extractor):
        self.text_processor = text_processor
        self.last_input = ""
        self.tokenized_input = []
        self.question_classifier = question_classifier
        self.data_manager = data_manager
        self.entity_extractor = entity_extractor
        self.remembered = False
        self.last_question_type = None

    def _read(self, input):
        self.last_question_type = self._get_question_type(input)
        self.last_input = input
        self.tokenized_input = self.text_processor.tokenize(self.last_input)
        self.data_manager.parse_input(self.tokenized_input)

        print('Last question type: ', self.last_question_type)
        if self.last_question_type == QuestionTypes.Declarative:
            isRemembered = self.data_manager.try_remember(self.tokenized_input)
            self.remembered = isRemembered

    def _answer(self):
        if self.last_question_type == QuestionTypes.Declarative:
            return self._answer_declarative()
        elif self.last_question_type == QuestionTypes.Informative:
            return self._answer_informative()

    def read_and_answer(self, input):
        if len(input) == 0:
            return 'You sent an empty string.'

        self._read(input)
        return self._answer()

    def _answer_informative(self):
        answer = self.data_manager.answer_from_database(self.tokenized_input)
        topic = self._get_topic(self.last_input)['topic']
        print('TOPIC: ')
        print(topic)

        if topic in ['HUM', 'ABBR'] and not answer:
            entities = self.entity_extractor.get_entities(self.last_input)

            print('ENTITIES:')
            print(entities)

            if entities:
                answer = self.data_manager.answer_from_wiki(
                    search_phrases=entities,
                    titles_per_phrase=1,
                    only_intro=True)

                print('HUM ASNWER:')
                print(answer)

        if not answer:
            search_phrases, nj_phrases = self.data_manager.get_search_phrases(self.tokenized_input)
            answer = self.data_manager.answer_from_wiki(
                search_phrases=search_phrases,
                titles_per_phrase=3,
                only_intro=False,
                nj_phrases=nj_phrases)

        if not answer or len(answer) == 0 or answer is None:
            answer = "I don't know. What do you think?"

        return answer

    def _answer_declarative(self):
        if self.remembered:
            return 'I learned that ' + self.last_input
        else:
            return 'Right back at you.'

    def _get_topic(self, question):
        return self.question_classifier.predict(question)

    def _get_question_type(self, utterance):
        mark = utterance[len(utterance) - 1]
        if mark == '.':
            return QuestionTypes.Declarative
        else:
            return QuestionTypes.Informative
