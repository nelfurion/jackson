class SvoExtractor():
    def __init__(self, text_processor, phrase_extractor):
        self.phrase_extractor = phrase_extractor
        self.text_processor = text_processor

    def is_full_svo(self, svo):
        return ('subject' in svo
                and 'verb' in svo
                and 'object' in svo
                and None not in svo.values())

    def is_full_sv(self, sv):
        return (
                'subject' in sv
                and 'verb' in sv
                and sv['subject'] is not None
                and sv['verb'] is not None)

    def get_svos(self, nltk_tree):
        trees = self._get_S_trees(nltk_tree)
        svos = []
        print('get_svos')
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


    def get_nj_phrases(self, tree):
        return self.phrase_extractor.extract(tree)

    def get_search_phrases(self, nj_phrases):
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