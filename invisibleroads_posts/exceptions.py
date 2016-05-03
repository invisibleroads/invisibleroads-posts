import json
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound


class HTTPErrorJSONMixin(object):

    def __init__(self, value_by_key):
        super(HTTPErrorJSONMixin, self).__init__()
        self.body = json.dumps(value_by_key)
        self.content_type = 'application/json'


class HTTPNotFoundJSON(HTTPErrorJSONMixin, HTTPNotFound):
    pass


class HTTPBadRequestJSON(HTTPErrorJSONMixin, HTTPBadRequest):
    pass
