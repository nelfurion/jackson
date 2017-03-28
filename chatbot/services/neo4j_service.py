from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

from .database_service import DatabaseService
from .config import config

class Neo4jService(DatabaseService):
    GET_REQUEST_FORMAT = 'MATCH (n) WHERE n.name="{name}" RETURN n'

    def __init__(
                self,
                url = config['db_url'],
                username = config['db_username'],
                password = config['db_password']):

        super().__init__()
        self.db = GraphDatabase(
                            url,
                            username=username,
                            password=password)

    def get(self, name):
        query = self._create_request(name)
        results = self.db.query(query, returns=(client.Node))
        if len(results) > 0:
            return results[0][0]

        return None

    def _relation_exists(self, first_node, second_node, label):
        relationships = first_node.relationships.all(types=[label])

        return second_node in [rel.end for rel in relationships]

    def add_relation(self, first, second, label):
        if not self._relation_exists(first, second, label):
            first.relationships.create(label, second)

    def add(self, name, **kwargs):
        node = self.get(name)

        if node:
            return node

        return self.db.nodes.create(name=name, **kwargs)

    def get_relations(self, node, label):
        return [rel.end.properties['name']
                for rel
                in node.relationships.outgoing(types=[label])]

    def _create_request(self, name):
        query = Neo4jService.GET_REQUEST_FORMAT.format(
            name=name
        )

        return query
