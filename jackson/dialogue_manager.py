from .question_types import QuestionTypes
from information_retrieval.parser import Parser

p = Parser()

class DialogueManager():
    def __init__(self, parser = p):
        self.parser = parser

    def process_input(self, tokenized_input):
        question_type = self.get_question_type(tokenized_input)
        if question_type == QuestionTypes.Declarative:
            tokenized_input.encode('ascii')
            parsed = self.parser.parse(tokenized_input)
            parsed.draw()
            svo = self._get_svo(parsed)

            print('subject: ', svo['subject'])
            print('verb: ', svo['verb'])
            print('object: ', svo['object'])

    def get_question_type(self, tokenized_input):
        return QuestionTypes.Declarative

    def answer(self):
        pass

    def ask(self):
        pass

    def _get_svo(self, bllip_tree):
        svo = {}
        for sentence_tree in bllip_tree:
            svo['subject'] = self._get_node_text(sentence_tree, 'NP')
            for node in sentence_tree:
                if hasattr(node, 'label'):
                    if 'VP' in node.label():
                        svo['verb'] = self._get_node_text(node, 'V')
                        svo['object'] = self._get_node_text(node, 'NP')
                        break

        return svo

    def _get_node_text(self, tree, nodeName):
        for node in tree:
            if hasattr(node, 'label'):
                if nodeName in node.label():
                    return ' '.join(node.leaves())