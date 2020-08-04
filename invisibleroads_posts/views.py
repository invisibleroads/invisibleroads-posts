import json
from pyramid.httpexceptions import HTTPBadRequest, HTTPException
from pyramid.view import exception_view_config


@exception_view_config(HTTPException)
def handle_exception(context, request):
    status_int = context.status_int
    response = request.response
    response.status_int = status_int
    if status_int in (400, 401, 403, 404):
        response.content_type = 'application/json'
        response.text = json.dumps(context.detail)
    return response


def expect_integer(
        request, key, parse=None, minimum=None, maximum=None, default=None):
    value = expect_value(
        request, key, int, 'expected integer', default=default)
    if parse:
        try:
            value = parse(value)
        except ValueError:
            raise HTTPBadRequest({key: 'unexpected value'})
    if minimum and value < minimum:
        raise HTTPBadRequest({key: 'expected value >= %s' % minimum})
    if maximum and value > maximum:
        raise HTTPBadRequest({key: 'expected value <= %s' % maximum})
    return value


def expect_value(request, key, parse=None, message=None, default=None):
    value = get_value(request, key, default)
    if parse:
        try:
            value = parse(value)
        except (KeyError, ValueError):
            raise HTTPBadRequest({key: message or 'bad'})
    return value


def get_value(request, key, default=None):
    try:
        return request.matchdict[key]
    except KeyError:
        pass
    try:
        return request.params[key]
    except KeyError:
        pass
    try:
        return request.json_body[key]
    except KeyError:
        pass
    if default is not None:
        return default
    raise HTTPBadRequest({key: 'required'})
