import sys
sys.path.append('../')
from decorators.abstract_method import abstract_method

class DataService:
    '''Abstract. Extract data from a database.'''

    @abstract_method
    def get(self, name):
        '''Returns a document whose name matches the given.'''
        pass

    @abstract_method
    def search(self, name):
        '''Searches for documents with the given name.'''
        pass

    @abstract_method
    def find(self, name):
        '''First searches for a document, then gets the matching one'''
        pass
