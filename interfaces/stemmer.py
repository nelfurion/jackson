from decorators.abstract_method import abstract_method

class Stemmer:
    def __init__(self):
        pass

    @abstract_method
    def stem(self, token):
        pass
