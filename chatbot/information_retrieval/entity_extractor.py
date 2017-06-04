class EntityExtractor():
    def __init__(self, text_processor):
        self.text_processor = text_processor

    def preprocess(self, text):
        sentences = self.text_processor.tokenize_sentences(text)
        tokenized_sentences = [self.text_processor.tokenize(sentence) for sentence in sentences]
        tagged_sentences = [self.text_processor.get_pos_tags(sentence) for sentence in tokenized_sentences]

        return tagged_sentences

    def get_entities(self, text):
        entities = []

        tagged_sentences = self.preprocess(text)
        chunked_sentences = self.text_processor.get_named_entity_chunks(tagged_sentences, binary=False)
        for sentence_tree in chunked_sentences:
            entities.extend(self.get_names_from_chunks(sentence_tree))

        return entities

    def get_names_from_chunks(self, chunk):
        entities = []
        if hasattr(chunk, 'label') and chunk.label:
            if chunk.label() != 'S':
                entities.append(' '.join([child[0] for child in chunk]))
            else:
                for child in chunk:
                    entities.extend(self.get_names_from_chunks(child))

        return entities