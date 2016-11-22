import json

from urllib.request import urlopen
from data_service import DataService

class WikipediaService(DataService):
    'A data service class for wikipedia.'

    ENDPOINT = 'https://en.wikipedia.org/w/api.php?'
    FORMAT = 'json'
    def __init__(self):
        pass

    def get(self, name):
        'Returns a document whose name matches the given.'

        requestUrl = self.create_request({
            'action': 'query',
            'titles': name,
            'prop': 'extracts',
            'exlimit': 'max',
            'explaintext' : None,
            'format': self.FORMAT
        })

        response = urlopen(requestUrl).read()
        response = response.decode('utf8')
        pages = json.loads(response)['query']['pages']

        print('Finished request: ', requestUrl, '...')

        return pages[list(pages)[0]]['extract']

    def search(self, name):
        'Searches for documents with the given name.'

        requestUrl = self.create_request({
            'action': 'opensearch',
            'search': name,
            'limit': 10,
            'format': self.FORMAT
        })

        response = urlopen(requestUrl).read()
        response = response.decode('utf8')

        print('Finished request: ', requestUrl, '...')

        return json.loads(response)

    def create_request(self, params):
        requestUrl = self.ENDPOINT
        for key, value in params.items():
            requestUrl += '&' + key

            if type(value) == str:
                value = value.replace(' ', '%20')

            if value is not None:
                requestUrl += '=' + str(value)

        return requestUrl
