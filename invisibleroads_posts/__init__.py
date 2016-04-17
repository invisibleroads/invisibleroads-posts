from os.path import basename
from pyramid.config import Configurator
from pyramid.path import AssetResolver
from pyramid.response import FileResponse
from pyramid.settings import aslist

from .libraries.cache import configure_cache, FUNCTION_CACHE
from .libraries.text import render_title
from .views import add_routes


def main(global_config, **settings):
    config = Configurator(settings=settings)
    includeme(config)
    return config.make_wsgi_app()


def includeme(config):
    configure_assets(config)
    configure_cache(config, FUNCTION_CACHE, 'server_cache.function.')
    configure_views(config)


def configure_assets(config):
    settings = config.registry.settings
    config.add_directive('add_root_asset', _add_root_asset)
    http_expiration_time = get_http_expiration_time(settings)
    for asset_spec in aslist(settings.get('website.root_assets', [])):
        config.add_root_asset(asset_spec, http_expiration_time)
    config.add_static_view(
        '_/invisibleroads-posts', 'invisibleroads_posts:assets',
        cache_max_age=http_expiration_time)


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


def get_http_expiration_time(settings):
    return int(settings.get('client_cache.http.expiration_time', 3600))


def _add_root_asset(config, asset_spec, http_cache):
    asset_path = AssetResolver().resolve(asset_spec).abspath()
    config.add_view(
        lambda request: FileResponse(asset_path, request),
        basename(asset_path), http_cache=http_cache)
