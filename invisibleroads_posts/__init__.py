import logging
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


LOG = logging.getLogger(__name__)


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
    add_fused_asset_view(config, 'site.min.css')
    add_fused_asset_view(config, 'site.min.js')


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


def add_fused_asset_view(config, view_name):
    LOG.debug('Generating %s' % view_name)
    settings = config.registry.settings
    file_name = view_name.replace('site', 'part')
    asset_parts = []
    for package_name in OrderedSet(aslist(settings['website.dependencies'])):
        asset_spec = '%s:assets/%s' % (package_name, file_name)
        asset_path = get_asset_path(asset_spec)
        if not exists(asset_path):
            LOG.debug('_ %s' % asset_spec)
            continue
        asset_parts.append(open(asset_path).read().strip())
        LOG.debug('+ %s' % asset_spec)
    asset_content = '\n'.join(asset_parts)
    content_type = mimetypes.guess_type(view_name)[0]
    http_expiration_time = get_http_expiration_time(settings)
    config.add_view(
        lambda request: Response(asset_content, content_type=content_type),
        view_name, http_cache=http_expiration_time)


def get_asset_path(asset_spec):
    return AssetResolver().resolve(asset_spec).abspath()


def get_http_expiration_time(settings):
    return int(settings.get('client_cache.http.expiration_time', 3600))
