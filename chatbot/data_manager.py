from information_retrieval.phrase_extractor import PhraseExtractor

class DataManager():
    ANSWER_FULL_FORMAT = '{subject} {verb} {related_nodes}'
    ANSWER_NO_RELATIONS_FORMAT = 'I know {subject}, but I don\'t know what {subject} {verb}.'

    def __init__(self, text_processor, db_service, wiki_service, search_service, parser):
        self.text_processor = text_processor
        self.db_service = db_service
        self.wiki_service = wiki_service
        self.search_service = search_service
        self.parser = parser

    def try_remember(self, tokenized_sentence):
        tree = self.parser.parse(tokenized_sentence)
        tree.draw()
        svos = self._get_svos(tree)

        remembered = False

        for svo in svos:
            print(svo)
            if self._is_full_svo(svo):
                relation = self.text_processor.lemmatize(svo['verb'], 'v')

                subject = self.db_service.add(
                    name=svo['subject'].lower(),
                    original_name=svo['subject'])

                object = self.db_service.add(
                    name=svo['object'].lower(),
                    original_name=svo['object'])

                self.db_service.add_relation(subject, object, relation.lower())

                remembered = True

        return remembered

    def try_answer(self, tokenized_sentence):
        print('TRY ANSER')
        tree = self.parser.parse(tokenized_sentence)
        svos = self._get_svos(tree)

        answer = None
        for svo in svos:
            print(svo)
            if self._is_full_sv(svo):
                self.text_processor.get_lemmas(svo['verb'], 'VERB')
                node = self.db_service.get(svo['subject'].lower())
                if node:
                    related_nodes = self.db_service.get_relations(node, svo['verb'].lower())
                    if related_nodes:
                        answer = self.ANSWER_FULL_FORMAT.format(
                            subject = svo['subject'],
                            verb = svo['verb'],
                            related_nodes = ', '.join(related_nodes)
                        )
                    else:
                        answer = self.ANSWER_NO_RELATIONS_FORMAT.format(
                            subject = svo['subject'],
                            verb = svo['verb']
                        )

        print(answer)

        return answer

    def _is_full_svo(self, svo):
        return ('subject' in svo
                and 'verb' in svo
                and 'object' in svo
                and None not in svo.values())

    def _is_full_sv(self, sv):
        return (
                'subject' in sv
                and 'verb' in sv
                and sv['subject'] is not None
                and sv['verb'] is not None)

    def _get_svos(self, bllip_tree):
        trees = self._get_S_trees(bllip_tree)
        svos = []
        for sentence_tree in trees:
            svo = {}
            svo['verb'] = ''
            svo['subject'] = self._get_noun_text(sentence_tree)
            for node in sentence_tree:
                if hasattr(node, 'label'):

                    if 'MD' in node.label():
                        svo['verb'] = ' '.join(node.leaves()) + ' ' + svo['verb']

                    if 'VP' in node.label():
                        svo['verb'] += self._get_verb_text(node).strip()
                        svo['object'] = self._get_noun_text(node)
                        if svo['object']:
                            svo['object'] = svo['object'].strip()

                        break

            svos.append(svo)

        return svos

    def _get_S_trees(self, bllip_tree):
        trees = []
        for node in bllip_tree:
            if hasattr(node, 'label'):
                if node.label() == 'S'\
                        or node.label() == 'SQ':
                    trees.append(node)

                trees.extend(self._get_S_trees(node))

        return trees

    def _get_verb_text(self, tree):
        text = ''
        for node in tree:
            if hasattr(node, 'label'):
                if 'V' in node.label()\
                        or 'MD' in node.label():
                    if len(node.leaves()) == 1:
                        text += ' '.join(node.leaves()) + ' '

                    text += self._get_verb_text(node)

        return text

    def _get_noun_text(self, tree):
        for node in tree:
            if hasattr(node, 'label'):
                if 'N' in node.label():
                    return ' '.join(node.leaves())

        text = ''
        for node in tree:
            if hasattr(node, 'label'):
                if 'VP' in node.label():
                    return self._get_noun_text(node)

    def _get_nj_phrases(self, tree):
        phrase_extractor = PhraseExtractor()
        nj_phrases = phrase_extractor.extract(tree)
        print('Extracted nouns:')
        print(nj_phrases[0])
        print('Extracted adjectives:')
        print(nj_phrases[1])
        return nj_phrases