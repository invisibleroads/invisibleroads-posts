import json
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound


class HTTPErrorJSONMixin(object):
    content_type = 'application/json'

    def __init__(self, value_by_key):
        super(HTTPErrorJSONMixin, self).__init__()
        self.body = json.dumps(value_by_key)


class HTTPNotFoundJSON(HTTPErrorJSONMixin, HTTPNotFound):
    pass


class HTTPBadRequestJSON(HTTPErrorJSONMixin, HTTPBadRequest):
    pass
