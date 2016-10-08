import simplejson as json
from pyramid.httpexceptions import HTTPBadRequest


def add_routes(config):
    settings = config.registry.settings

    config.add_route('index', '')

    config.add_view(
        renderer='invisibleroads_posts:templates/posts.jinja2',
        route_name='index')
    config.add_notfound_view(
        handle_page_not_found, renderer=settings.get(
            'website.page_not_found_template',
            'invisibleroads_posts:templates/404.jinja2'))
    config.add_view(handle_bad_request, context=HTTPBadRequest)


def expect_param(key, params, parse=None, message=''):
    try:
        value = params[key]
    except KeyError:
        raise HTTPBadRequest({key: 'required'})
    if parse:
        try:
            value = parse(value)
        except ValueError:
            raise HTTPBadRequest({key: message or 'unparseable'})
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
