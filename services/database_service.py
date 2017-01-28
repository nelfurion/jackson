from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

class DatabaseService():
    def __init__(self):
        self.db = GraphDatabase("http://hobby-gbmnkacijildgbkegogbbmol.dbs.graphenedb.com:24789/db/data/",
                            username="jackson",
                            password="oDOHS8F01PHBZA5jkr8P")

    def get(self, name):
        q = 'MATCH (n) WHERE n.name="' + name + '" RETURN n'
        results = self.db.query(q, returns=(client.Node))
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