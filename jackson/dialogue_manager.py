from .question_types import QuestionTypes

class DialogueManager():
    def __init__(self, parser, db_service):
        self.parser = parser
        self.db_service = db_service

    def process_input(self, tokenized_input):
        question_type = self.get_question_type(tokenized_input)
        if question_type == QuestionTypes.Declarative:
            tokenized_input.encode('ascii')

            parsed.draw()
            svo = self._get_svo(parsed)

            if self.isFullSvo(svo):
                print('subject: ', svo['subject'])
                print('verb: ', svo['verb'])
                print('object: ', svo['object'])
                self.db_service



    def answer(self):
        pass

    def ask(self):
        pass