import nltk

class NltkEntityExtractor():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def preprocess(self, text):
        sentences = self.tokenizer.tokenize_sentences(text)
        tokenized_sentences = [self.tokenizer.tokenize_words(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

        return tagged_sentences

    def get_entities(self, text):
        entities = []

        tagged_sentences = self.preprocess(text)
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)
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