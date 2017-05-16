from .sentence_scorer import SentenceScorer
from preprocess.lemmatizer import Lemmatizer
from preprocess.tokenizer import Tokenizer
from .phrase_extractor import PhraseExtractor
from .parser import Parser

import sys
import importlib

class SummarizationTask:
    def __init__(self, arguments):
        self.arguments = arguments

    def __call__(self):
        # Reloading the whole module, because it is not thread safe
        if 'preprocess.lemmatizer' in sys.modules:
            importlib.reload(sys.modules['preprocess.lemmatizer'])

        sentence_scorer = SentenceScorer(
            Lemmatizer(),
            Tokenizer(),
            Parser.get_instance(),
            PhraseExtractor())

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