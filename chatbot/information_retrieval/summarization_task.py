import sys
import importlib
from sklearn.externals import joblib

from information_retrieval.config import config
from information_retrieval.sentence_scorer import SentenceScorer
from information_retrieval.phrase_extractor import PhraseExtractor
from preprocess.text_processor import TextProcessor
from preprocess.lemmatizer import Lemmatizer
from preprocess.stemmer import Stemmer
from preprocess.tokenizer import Tokenizer
from preprocess.tagged_words_corpus import TaggedWordsCorpus

from information_retrieval.parser import Parser


class SummarizationTask:
    def __init__(self, arguments):
        self.arguments = arguments

    def __call__(self):
        # Reloading the whole module, because it is not thread safe
        if 'preprocess.lemmatizer' in sys.modules:
            importlib.reload(sys.modules['preprocess.lemmatizer'])

        text_processor = TextProcessor(
            lemmatizer= Lemmatizer(),
            parser= Parser.get_instance(),
            stemmer= Stemmer(),
            tokenizer= Tokenizer(),
            vectorizer= joblib.load(config['vectorizer']),
            tagged_words_corpus= TaggedWordsCorpus()
        )

        phrase_extractor = PhraseExtractor(text_processor)

        sentence_scorer = SentenceScorer(
            text_processor=text_processor,
            phrase_extractor=phrase_extractor)

        result = sentence_scorer.score_sentences_by_input_phrases(**self.arguments)
        title_nj_phrases = sentence_scorer.get_title_phrases(self.arguments['title'])
        title_score_and_matches = sentence_scorer.score_title(title_nj_phrases, self.arguments['nj_phrases'])
        title_score = title_score_and_matches[0]

        for i in range(len(result)):
            old_tuple = result[i]
            new_tuple = (
                old_tuple[0],
                old_tuple[1],
                old_tuple[2] + title_score)

            result[i] = new_tuple

        return result