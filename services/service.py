class Service():
    """Abstract service class."""
    def _create_request(self, params, endpoint):
        request_url = endpoint
        for key, value in params.items():
            request_url += '&' + key

            if type(value) == str:
                value = value.replace(' ', '%20')

            if value is not None:
                request_url += '=' + str(value)

        return request_url
