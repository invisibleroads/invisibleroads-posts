from os.path import exists, join
from pyramid.response import FileResponse

from .exceptions import HTTPBadRequestJSON


def add_routes(config):
    config.add_route('index', '')
    config.add_view(
        list_posts, renderer='invisibleroads_posts:templates/posts.jinja2',
        route_name='index')


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
        raise HTTPBadRequestJSON({key: 'required'})
