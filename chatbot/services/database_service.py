from .service import Service

class DatabaseService(Service):
    def __init__(self):
        super().__init__()

    def get(self, name):
        pass

    def _relation_exists(self, first_node, second_node, label):
        pass

    def add_relation(self, first, second, label):
        pass

    def add(self, name, **kwargs):
        pass

    def get_relations(self, node, label):
        pass
