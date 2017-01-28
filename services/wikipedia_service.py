import json
import re

from urllib.request import urlopen

from . import wiki_skip

class WikipediaService():
    'A data service class for wikipedia.'

    ENDPOINT = 'https://en.wikipedia.org/w/api.php?'
    FORMAT = 'json'
    header_expression = re.compile(wiki_skip.HEADER_PATTERN)

    def __init__(self):
        pass

    def search(self, name):
        'Searches for page names.'
        request_url = self.create_request({
            'action': 'query',
            'format': self.FORMAT,
            'srsearch': name,
            'list': 'search',
        })

        print('SEARCHING FOR: ', request_url)

        response = urlopen(request_url).read()
        response = response.decode('utf-8')

        response = json.loads(response)
        page_infos = response['query']['search']

        page_titles = []
        for info in page_infos:
            should_add = True
            title = info['title']
            for substring in wiki_skip.TITLE_SUBSTRINGS:
                if substring in title:
                    should_add = False
                    break

            if should_add:
                page_titles.append(title)

        return page_titles

    def find(self, name):
        try:
            print('WIKI: find -> ', name)
            page_titles = self.search(name)
            print('A'*30)
            print(page_titles)
            full_text = ''
            for title in page_titles:
                full_text += self.get(title)

            return full_text
        except IndexError as e:
            print('WIKI SERVICE: ' + e)
            return ''

    def get(self, page_title):
        'Returns a document whose name matches the given.'

        request_url = self.create_request({
            'action': 'query',
            'format': self.FORMAT,
            'titles': page_title,
            'prop': 'extracts',
            'exlimit': 'max',
            'explaintext': '1',
            'redirects': '1'
        })

        response = urlopen(request_url).read()
        response = response.decode('utf-8')
        #print('PAGE TITLE: ', page_title)
        pages = json.loads(response)['query']['pages']
        #print(pages)

        print('PAGES LENGTH: ', len(pages))

        result_text = ''
        for page_id in pages:

            print('HERE 1')

            if len(pages[page_id]['extract']) > 0:
                print('HERE 1.2')
                page_extract = pages[page_id]['extract']
                print('HERE 1.3')
                headers = list(self.header_expression.finditer(page_extract))

                print('HERE 2')

                if len(headers) == 0 or len(headers[0].span()) == 0:
                    print('HERE 3')
                    #Page doesn't have a useful content.
                    continue

                print('HERE 4')

                result_text += page_extract[0:headers[0].span()[0]]
                for i in range(len(headers)):
                    current_header = headers[i]
                    current_paragraph_index = current_header.span()[0] + 1
                    next_header_index = len(page_extract)

                    print('HERE 5')

                    if i + 1 < len(headers):
                        next_header = headers[i + 1]
                        next_header_index = next_header.span()[0]

                        print('HERE 6')


                    if not self._should_skip_header(
                            current_header.group(1),
                            current_paragraph_index,
                            next_header_index):
                        result_text += page_extract[
                                       current_paragraph_index
                                       :
                                       next_header_index]

                        print('HERE 7')

                    print('HERE 8')
            print('HERE 9')

        print('Finished request: ', request_url, '...')

        return result_text

    def create_request(self, params):
        request_url = self.ENDPOINT
        for key, value in params.items():
            request_url += '&' + key

            if type(value) == str:
                value = value.replace(' ', '%20')

            if value is not None:
                request_url += '=' + str(value)

        return request_url

    def _should_skip_header(self, header, paragraph_index, next_header_index):
        header = header.lower()
        for substring in wiki_skip.SUBSTRINGS:
            if substring in header:
                return True

        return False