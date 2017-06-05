import json
import re

from urllib.request import urlopen

from . import wiki_skip

class WikipediaService():
    'A data service class for wikipedia.'

    ENDPOINT = 'https://en.wikipedia.org/w/api.php?'
    FORMAT = 'json'

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
            print('IndexError: ', e)
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

    def _find_headers(self, text_lines):
        header_indexes = []
        for i in range(len(text_lines)):
            line = text_lines[i]
            if len(line) > 0:
                line_end = line[len(line) - 1]
                if line[0] == '=' and line_end == '=':
                    header_indexes.append(i)

        return header_indexes

    def _get_text_from_pages(self, pages):
        result_text = ''
        for page_id in pages:
            if 'extract' in pages[page_id].keys():
                if len(pages[page_id]['extract']) > 0:
                    page_extract = pages[page_id]['extract']
                    lines = page_extract.split('\n')
                    header_indexes = self._find_headers(lines)

                    if len(header_indexes) == 0:
                        # Page doesn't have a useful content.
                        continue

                    result_text += self._get_headers_content(header_indexes, lines)

        return result_text

    def _get_headers_content(self, header_indexes, page_extract_lines):
        previous_header_index = header_indexes[0]
        previous_header = page_extract_lines[previous_header_index]
        result_lines = page_extract_lines[0:previous_header_index]
        for i in range(1, len(header_indexes)):
            if not self._should_skip_header(previous_header):
                extract_from = previous_header_index + 1
                extract_until = header_indexes[i]
                extract_lines = page_extract_lines[extract_from:extract_until]
                result_lines.extend(extract_lines)

            previous_header_index = header_indexes[i]
            previous_header = page_extract_lines[previous_header_index]

        return '\n'.join(result_lines)

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

    def _should_skip_header(self, header):
        header = header.lower()
        for substring in wiki_skip.SUBSTRINGS:
            if substring in header:
                return True

        return False