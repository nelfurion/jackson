from information_retrieval.phrase_extractor import PhraseExtractor
from information_retrieval.summarizer import Summarizer
from preprocess.lemmatizer import Lemmatizer
summarizer = Summarizer(Lemmatizer())

class DataManager():
    ANSWER_FULL_FORMAT = '{subject} {verb} {related_nodes}.'
    ANSWER_NO_RELATIONS_FORMAT = 'I know {subject}, but I don\'t know what {subject} {verb}.'
    TITLES_PER_PHRASE = 2

    def __init__(self, text_processor, db_service, wiki_service, search_service, parser):
        self.text_processor = text_processor
        self.db_service = db_service
        self.wiki_service = wiki_service
        self.search_service = search_service
        self.parser = parser

    def try_remember(self, tokenized_sentence):
        print(tokenized_sentence)
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
        tree = self.parser.parse(tokenized_sentence)
        svos = self._get_svos(tree)
        tree.draw()
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
                            verb = svo['verb'].lower(),
                            related_nodes = ', '.join(related_nodes)
                        )
                    else:
                        answer = self.ANSWER_NO_RELATIONS_FORMAT.format(
                            subject = svo['subject'],
                            verb = svo['verb']
                        )

        print('ANSWER: ', answer, '-'*30)

        return answer

    def answer_from_wiki(self, tokenized_sentence):
        tree = self.parser.parse(tokenized_sentence)
        nj_phrases = self._get_nj_phrases(tree)
        search_phrases = self._get_search_phrases(nj_phrases)

        page_titles = []
        for search_phrase in search_phrases:
            titles = self.wiki_service.search(search_phrase)[:DataManager.TITLES_PER_PHRASE]
            page_titles.extend(titles)

        print(page_titles)

        full_text = ''
        for title in page_titles:
            print('GETTING PAGE FOR TITLE: ', title)
            full_text += self.wiki_service.get(title)
            print('GET FINISHED: ', title)

        return summarizer.summarize_by_input_frequency(3, full_text, nj_phrases)

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
        print('get_svos')
        for sentence_tree in trees:

            sentence_tree.draw()
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
                    noun_subtrees = node.subtrees(self._noun_filter)
                    noun_subtrees = sorted(noun_subtrees, key=lambda x: x.height())
                    largest_subtree = noun_subtrees[-1]

                    return ' '.join(largest_subtree.leaves())

        text = ''
        for node in tree:
            if hasattr(node, 'label'):
                if 'VP' in node.label():
                    return self._get_noun_text(node)

    def _noun_filter(self, tree):
        passes = True
        if hasattr(tree, 'label'):
            if 'V' in tree.label():
                return False

        if type(tree) == str:
            return True

        for node in tree:
            if hasattr(node, 'label'):
                if 'V' in node.label():
                    return False

            passes = self._noun_filter(node)

        return passes


    def _get_nj_phrases(self, tree):
        phrase_extractor = PhraseExtractor()
        return phrase_extractor.extract(tree)

    def _get_search_phrases(self, nj_phrases):
        search_phrases = set()

        print(nj_phrases)

        noun_synonyms = set()
        for noun in nj_phrases['nouns']:
            synonyms = self.text_processor.get_synonyms(noun, 'n', 0.5)
            noun_synonyms.union(synonyms)

        nj_phrases['nouns'].union(noun_synonyms)

        adjective_synonyms = set()
        for adjective in nj_phrases['adjectives']:
            synonyms = self.text_processor.get_synonyms(adjective, 'a', 0.5)
            adjective_synonyms.union(synonyms)

        nj_phrases['adjectives'].union(adjective_synonyms)

        for noun in nj_phrases['nouns']:
            search_phrases.add(noun)
            for adjective in nj_phrases['adjectives']:
                search_phrases.add(adjective + ' ' + noun)

            for adjective_phrase in nj_phrases['adjective_phrases']:
                search_phrases.add(adjective_phrase + ' ' + noun)

        for noun_phrase in nj_phrases['noun_phrases']:
            search_phrases.add(noun_phrase)
            for adjective in nj_phrases['adjectives']:
                search_phrases.add(adjective + ' ' + noun_phrase)

            for adjective_phrase in nj_phrases['adjective_phrases']:
                search_phrases.add(adjective_phrase + ' ' + noun_phrase)

        print('SEARCH PHRASES')
        print(search_phrases)

        return search_phrases

    def _create_score_dict(self, words, scores):
        return {
                'words': [
                {
                    'word': words[i],
                    'score': scores[i]
                }
                for i in range(len(words))]
        }