from decorators.abstract_method import abstract_method

class EntityExtractor():
    """An interface for an entity extractor. Extract entities from text."""
    @abstract_method
    def get_entities(text):
        pass

    @abstract_method
    def get_dates(text):
        pass
