import json

from urllib.request import urlopen
from services.data_service import DataService

class WikipediaService(DataService):
    'A data service class for wikipedia.'

    ENDPOINT = 'https://en.wikipedia.org/w/api.php?'
    FORMAT = 'json'
    def __init__(self):
        pass

    def get(self, name, part='intro'):
        'Returns a document whose name matches the given.'

        request_url = self.create_request({
            'action': 'query',
            'titles': name,
            'prop': 'extracts',
            'exlimit': 'max',
            'explaintext' : None,
            'format': self.FORMAT
        })

        #if a part of the page is not specified, return the intro
        if part == 'intro':
            request_url += '&exintro'

        response = urlopen(request_url).read()
        response = response.decode('utf-8')
        pages = json.loads(response)['query']['pages']

        print('Finished request: ', request_url, '...')

        return pages[list(pages)[0]]['extract']

    def search(self, name):
        'Searches for documents with the given name.'

        request_url = self.create_request({
            'action': 'opensearch',
            'search': name,
            'limit': 10,
            'format': self.FORMAT
        })

        response = urlopen(request_url).read()
        response = response.decode('utf-8')

        print('Finished request: ', request_url, '...')

        return json.loads(response)

    def find(self, name):
        search_result = self.search(name)
        page_name = search_result[1][0]
        return self.get(page_name)

    def create_request(self, params):
        request_url = self.ENDPOINT
        for key, value in params.items():
            request_url += '&' + key

            if type(value) == str:
                value = value.replace(' ', '%20')

            if value is not None:
                request_url += '=' + str(value)

        return request_url
