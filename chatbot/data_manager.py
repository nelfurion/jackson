class DataManager():
    def __init__(self, db_service, wiki_service, search_service, parser):
        self.db_service = db_service
        self.wiki_service = wiki_service
        self.search_service = search_service
        self.parser = parser

    def try_remember(self, tokenized_sentence):
        tree = self.parser.parse(tokenized_sentence)
        svos = self._get_svos(tree)

        remembered = False

        for svo in svos:
            if self._is_full_svo(svo):
                subject = self.db_service.add(svo['subject'])
                object = self.db_service.add(svo['object'])
                self.db_service.add_relation(subject, object, svo['verb'])
                remembered = True

        return remembered

    def try_answer(self, tokenized_sentence):
        tree = self.parser.parse(tokenized_sentence)
        svos = self._get_svos(tree)

        #for svo in svos:
        #    print(svo)

        #print(tree)
        #tree.draw()

        #if self._is_full_svo(svo):
        #    print(svo)

        return None

    def _is_full_svo(self, svo):
        return ('subject' in svo
                and 'verb' in svo
                and 'object' in svo
                and None not in svo.values())

    def _get_svos(self, bllip_tree):
        trees = self._get_S_trees(bllip_tree)
        svos = []
        for sentence_tree in trees:
            svo = {}
            svo['subject'] = self._get_node_text(sentence_tree, 'NP')
            for node in sentence_tree:
                if hasattr(node, 'label'):
                    if 'VP' in node.label():
                        svo['verb'] = self._get_node_text(node, 'V')
                        svo['object'] = self._get_node_text(node, 'NP')
                        break

            svos.append(svo)

        return svos

    def _get_S_trees(self, bllip_tree):
        trees = []
        for node in bllip_tree:
            if hasattr(node, 'label'):
                if node.label() == 'S':
                    trees.append(node)

                trees.extend(self._get_S_trees(node))

        return trees

    def _get_node_text(self, tree, nodeName):
        for node in tree:
            if hasattr(node, 'label'):
                if nodeName in node.label():
                    return ' '.join(node.leaves())