import simplejson as json
from os.path import exists, join
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import FileResponse


def add_routes(config):
    config.add_route('index', '')
    config.add_view(
        list_posts, renderer='invisibleroads_posts:templates/posts.jinja2',
        route_name='index')
    config.add_view(is_bad_request, context=HTTPBadRequest)


def list_posts(request):
    settings = request.registry.settings
    path = join(settings['data.folder'], 'index.html')
    if not exists(path):
        return dict()
    return FileResponse(path, request)


def expect_param(key, params):
    try:
        return params[key]
    except KeyError:
        raise HTTPBadRequest({key: 'required'})


def is_bad_request(context, request):
    response = request.response
    response.body = json.dumps(context.detail).encode('utf-8')
    response.status_int = context.status_int
    response.content_type = 'application/json'
    return response
