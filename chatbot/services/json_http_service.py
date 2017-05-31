import requests
from services.http_service import HttpService

class JsonHttpService(HttpService):
    def get(self, endpoint, arguments):
        response = requests.get(endpoint, params=arguments)
        return response.json()

    def post(self, endpoint, body, arguments = {}):
        response = requests.post(endpoint, params=arguments, json=body)
        return response.json()