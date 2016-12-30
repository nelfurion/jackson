import nltk

from information_retrieval.entity_extractor import EntityExtractor

class NltkEntityExtractor(EntityExtractor):
    """Uses nltk to extract entities from text. Implements EntityExtractor."""

    def preprocess(self, text):
        sentences = nltk.sent_tokenize(text)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

        return tagged_sentences

    def get_entities(self, text):
        entities = []

        tagged_sentences = self.preprocess(text)
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)
        for sentence_tree in chunked_sentences:
            #sentence_tree.draw()
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

    def get_dates(text):
        pass
