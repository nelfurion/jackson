from classification.classifier import Classifier
from classification.text_processor import TextProcessor
from preprocess.stemmer import Stemmer
from preprocess.tokenizer import Tokenizer

text_processor = TextProcessor(Stemmer(), Tokenizer())
classifier = Classifier(text_processor)

while True:
    user_input = input()
    print(classifier.classify(user_input))
