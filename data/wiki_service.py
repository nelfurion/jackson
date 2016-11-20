from data_service import DataService

class ClassName(DataService):
    "A data service class for wikipedia."
    ENDPOINT = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=max&explaintext&titles=Google&format=jsonfm'

    def __init__(self):

    def get(self, name):
        'Returns a document whose name matches the given.'
        pass

    def search(self, name):
        'Searches for documents with the given name.'
        create_request({
            "action": "query",

        })

    def create_request(params):
        requestUrl = ENDPOINT
        for key, value in params.items():
            requestUrl += '&' + key + '=' + value
