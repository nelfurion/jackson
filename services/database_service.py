from neo4jrestclient.client import GraphDatabase
from .data_service import DataService

class DatabaseService(DataService):
    def __init__(self):
        self.db = GraphDatabase("http://hobby-gbmnkacijildgbkegogbbmol.dbs.graphenedb.com:24789/db/data/",
                            username="jackson",
                            password="oDOHS8F01PHBZA5jkr8P")
        pass

    def get(self, name):
        '''Returns a document whose name matches the given.'''
        pass

    def search(self, name):
        '''Searches for documents with the given name.'''
        pass

    def find(self, name):
        '''First searches for a document, then gets the matching one'''
        pass

    def init_autism(self):
        alice = self.db.nodes.create(name="Alice", age=30)