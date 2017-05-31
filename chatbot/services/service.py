from services.json_http_service import JsonHttpService

class Service():
    """Abstract service class."""
    def __init__(self, http_service = JsonHttpService()):
        self.http_service = http_service

    def get(self, endpoint, arguments):
        return self.http_service.get(endpoint, arguments)

    def post(self, endpoint, body, arguments = {}):
        return self.http_service.post(endpoint, body, arguments)