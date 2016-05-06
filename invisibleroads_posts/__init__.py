import mimetypes
from invisibleroads_macros.iterable import OrderedSet
from os.path import basename, exists
from pyramid.config import Configurator
from pyramid.path import AssetResolver
from pyramid.response import FileResponse, Response
from pyramid.settings import aslist

from .libraries.cache import configure_cache, FUNCTION_CACHE
from .libraries.text import render_title
from .views import add_routes


def main(global_config, **settings):
    config = Configurator(settings=settings)
    includeme(config)
    return config.make_wsgi_app()


def includeme(config):
    configure_cache(config, FUNCTION_CACHE, 'server_cache.function.')
    configure_assets(config)
    configure_views(config)


def configure_assets(config):
    settings = config.registry.settings
    http_expiration_time = get_http_expiration_time(settings)
    config.add_static_view(
        '_/invisibleroads-posts', 'invisibleroads_posts:assets',
        cache_max_age=http_expiration_time)
    # Add root assets
    for asset_spec in aslist(settings.get('website.root_assets', [])):
        asset_path = get_asset_path(asset_spec)
        asset_name = basename(asset_path)
        config.add_view(
            lambda request, x=asset_path: FileResponse(x, request),
            asset_name, http_cache=http_expiration_time)
    # Add fused assets
    add_fused_asset_view(config, 'site.min.css', 'website.style_assets')
    add_fused_asset_view(config, 'site.min.js', 'website.script_assets')


def configure_views(config):
    settings = config.registry.settings
    config.include('pyramid_jinja2')
    config.commit()
    config.get_jinja2_environment().globals.update({
        'website_name': settings.get('website.name', 'InvisibleRoads'),
        'website_sections': aslist(settings.get('website.sections', '')),
        'render_title': render_title,
    })
    add_routes(config)


def add_fused_asset_view(config, view_name, setting_key):
    print('Generating %s' % view_name)
    settings = config.registry.settings
    http_expiration_time = get_http_expiration_time(settings)
    content_type = mimetypes.guess_type(view_name)[0]
    asset_parts = []
    for asset_spec in OrderedSet(aslist(settings.get(setting_key, []))):
        if not asset_spec:
            continue
        asset_path = get_asset_path(asset_spec)
        if not exists(asset_path):
            print('_ %s' % asset_spec)
            continue
        asset_parts.append(open(asset_path).read().strip())
        print('+ %s' % asset_spec)
    asset_content = '\n'.join(asset_parts)
    config.add_view(
        lambda request: Response(asset_content, content_type=content_type),
        view_name, http_cache=http_expiration_time)


def get_asset_path(asset_spec):
    return AssetResolver().resolve(asset_spec).abspath()


def get_http_expiration_time(settings):
    return int(settings.get('client_cache.http.expiration_time', 3600))
