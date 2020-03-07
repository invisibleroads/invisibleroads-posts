import simplejson as json
from pyramid.httpexceptions import HTTPBadRequest, HTTPException
from pyramid.view import exception_view_config


def add_routes(config):
    config.add_route('index', '')

    config.add_view(
        renderer='invisibleroads_posts:templates/posts.jinja2',
        route_name='index')


def expect_param(request, key, parse=None, message=None, default=None):
    params = request.params
    try:
        value = params[key]
    except KeyError:
        if default is not None:
            value = default
        else:
            raise HTTPBadRequest({key: 'required'})
    if parse:
        try:
            value = parse(value)
        except (KeyError, ValueError):
            raise HTTPBadRequest({key: message or 'bad'})
    return value


def expect_integer(
        request, key, parse=None, minimum=None, maximum=None, default=None):
    value = expect_param(
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


@exception_view_config(HTTPException)
def handle_exception(context, request):
    status_int = context.status_int
    response = request.response
    response.status_int = status_int
    if status_int == 400:
        response.content_type = 'application/json'
        response.text = json.dumps(context.detail)
    return response
