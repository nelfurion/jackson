class DataManager():
    def __init__(self, db_service, wiki_service, search_service, parser):
        self.db_service = db_service
        self.wiki_service = wiki_service
        self.search_service = search_service
        self.parser = parser

    def try_remember(self, tokenized_sentence):
        tree = self.parser.parse(tokenized_sentence)
        svo = self._get_svo(tree)
        if self._is_full_svo(svo):
            subject = self.db_service.add(svo['subject'])
            object = self.db_service.add(svo['object'])
            self.db_service.add_relation(subject, object, svo['verb'])

            print(subject)
            print(object)

            return True

        return False

    def _is_full_svo(self, svo):
        return 'subject' in svo and 'verb' in svo and 'object' in svo

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