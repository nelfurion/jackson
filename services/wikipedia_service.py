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

        response = self._send_request({
            'action': 'query',
            'format': self.FORMAT,
            'srsearch': name,
            'list': 'search',
        })

        if not response:
            return []

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
            page_titles = self.search(name)
            full_text = ''
            for title in page_titles:
                full_text += self.get(title)

            return full_text
        except IndexError as e:
            print('WIKI SERVICE: ' + e)
            return ''

    def get(self, page_title, exintro = False):
        'Returns a document whose name matches the given.'

        request_params = {
            'action': 'query',
            'format': self.FORMAT,
            'titles': page_title,
            'prop': 'extracts',
            'exlimit': 'max',
            'explaintext': '1',
            'redirects': '1',
        }

        if exintro:
            request_params['exintro'] = '1'

        response = self._send_request(request_params)

        if not response:
            return ''

        pages = response['query']['pages']

        if exintro:
            return self._get_text_from_intros(pages)
        else:
            return self._get_text_from_pages(pages)

    def _get_text_from_intros(self, pages):
        full_text = ''
        for page_id in pages:
            full_text += pages[page_id]['extract']

        return full_text

    def _get_text_from_pages(self, pages):
        result_text = ''
        for page_id in pages:
            if len(pages[page_id]['extract']) > 0:
                page_extract = pages[page_id]['extract']
                headers = list(self.header_expression.finditer(page_extract))

                if len(headers) == 0 or len(headers[0].span()) == 0:
                    # Page doesn't have a useful content.
                    continue

                result_text += self._get_headers_content(headers, page_extract)

        return result_text

    def _get_headers_content(self, headers, page_extract):
        result_text = page_extract[0:headers[0].span()[0]]

        for i in range(len(headers)):
            current_header = headers[i]
            current_paragraph_index = current_header.span()[0] + 1
            next_header_index = len(page_extract)

            if i + 1 < len(headers):
                next_header = headers[i + 1]
                next_header_index = next_header.span()[0]

            if not self._should_skip_header(
                    current_header.group(1),
                    current_paragraph_index,
                    next_header_index):
                result_text += page_extract[
                               current_paragraph_index
                               :
                               next_header_index]

        return result_text

    def _send_request(self, options):
        try:
            request_url = self._create_request(options)
            print('Sending request to:')
            print(request_url)
            response = urlopen(request_url).read()
            response = response.decode('utf-8')
            response = json.loads(response)

            return response
        except UnicodeEncodeError as e:
            print('UnicodeEncodeError: ', e)
            return None

    def _create_request(self, params):
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