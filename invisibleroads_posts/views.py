import simplejson as json
from os.path import exists, join
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import FileResponse


def add_routes(config):
    config.add_route('index', '')
    config.add_view(
        index,
        renderer='invisibleroads_posts:templates/posts.jinja2',
        route_name='index')
    config.add_view(is_bad_request, context=HTTPBadRequest)
    # add_fused_asset_view(config, 'site.min.css')
    # add_fused_asset_view(config, 'site.min.js')


def index(request):
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


"""
def add_fused_asset_view(config, view_name):

    config.add_view(
        lambda request: Response(
            asset_content,
            content_type=content_type,
            charset='utf-8'),
        view_name,
        http_cache=http_expiration_time)

    asset_content = FUNCTION_CACHE.get(view_name, ignore_expiration=True)
    FUNCTION_CACHE.get_or_create(view_name, creator, expiration_time=-1)


def make_fused_asset_content
def fuse_asset_content
def fuse_asset

def get_fused_asset
def show_fused_asset
def fuse_asset
def render_fused_asset
"""
