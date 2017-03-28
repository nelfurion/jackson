from django.http import JsonResponse

from ..classification.classifier import Classifier
from ..classification.text_processor import TextProcessor
from ..preprocess.stemmer import Stemmer
from ..preprocess.tokenizer import Tokenizer

def get_topic(request):
    text_processor = TextProcessor(Stemmer(), Tokenizer())
    classifier = Classifier(text_processor)

    question = request.GET.get('question', '')
    topic = classifier.classify(question)[0]

    response = JsonResponse({
        "topic": topic
    })

    return response
