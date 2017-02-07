import simplejson as json
from pyramid.httpexceptions import HTTPBadRequest


def add_routes(config):
    settings = config.registry.settings

    config.add_route('index', '')

    config.add_view(
        renderer='invisibleroads_posts:templates/posts.jinja2',
        route_name='index')
    config.add_view(handle_bad_request, context=HTTPBadRequest)
    config.add_notfound_view(handle_page_not_found, renderer=settings[
        'website.page_not_found_template'])


def expect_integer(
        key, params, validate=None, minimum_value=None, maximum_value=None):
    value = expect_param(key, params, int, 'expected integer')
    if validate and not validate(value):
        raise HTTPBadRequest({key: 'unexpected value'})
    if minimum_value and value < minimum_value:
        raise HTTPBadRequest({key: 'expected value >= %s' % minimum_value})
    if maximum_value and value > maximum_value:
        raise HTTPBadRequest({key: 'expected value <= %s' % maximum_value})
    return value


def expect_param(key, params, parse=None, message=''):
    try:
        value = params[key]
    except KeyError:
        raise HTTPBadRequest({key: 'required'})
    if parse:
        try:
            value = parse(value)
        except ValueError:
            raise HTTPBadRequest({key: message or 'unexpected value'})
    return value


def handle_bad_request(context, request):
    response = request.response
    response.status_int = context.status_int
    response.content_type = 'application/json'
    response.body = json.dumps(context.detail).encode('utf-8')
    return response


def handle_page_not_found(request):
    response = request.response
    response.status_int = 404
    return {}
