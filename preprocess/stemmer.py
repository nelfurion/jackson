from decorators.abstract_method import abstract_method

class Stemmer:
    @abstract_method
    def stem(self, token):
        pass
