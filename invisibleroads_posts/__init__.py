import logging
import mimetypes
from invisibleroads_macros.iterable import OrderedSet, set_default
from os.path import abspath, basename, exists
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
    add_routes_for_fused_assets(config)
    return config.make_wsgi_app()


def includeme(config):
    configure_settings(config)
    configure_cache(config, FUNCTION_CACHE, 'server_cache.function.')
    configure_assets(config)
    configure_views(config)


def configure_settings(config):
    settings = config.registry.settings

    http_expiration_time = set_default(
        settings, 'client_cache.http.expiration_time', 3600, int)
    config.add_directive(
        'add_cached_static_view',
        lambda config, *arguments, **keywords: config.add_static_view(
            *arguments, cache_max_age=http_expiration_time, **keywords))
    config.add_directive(
        'add_cached_view',
        lambda config, *arguments, **keywords: config.add_view(
            *arguments, http_cache=http_expiration_time, **keywords))

    set_default(settings, 'website.dependencies', [], aslist)
    settings['website.dependencies'].append(config.package_name)


def configure_assets(config):
    settings = config.registry.settings
    config.add_cached_static_view(
        '_/invisibleroads-posts', 'invisibleroads_posts:assets')
    for asset_spec in aslist(settings.get('website.root_assets', [])):
        asset_path = get_asset_path(asset_spec)
        asset_name = basename(asset_path)
        config.add_cached_view(
            lambda request, x=asset_path: FileResponse(x, request), asset_name)


def configure_views(config):
    settings = config.registry.settings
    config.include('pyramid_jinja2')
    config.commit()
    config.get_jinja2_environment().globals.update({
        'website_name': settings.get('website.name', 'InvisibleRoads'),
        'website_owner': settings.get('website.owner', 'InvisibleRoads'),
        'website_url': settings.get('website.url', '/#'),
        'base_template': settings.get(
            'website.base_template',
            'invisibleroads_posts:templates/base.jinja2'),
        'render_title': render_title,
    })
    add_routes(config)


def add_routes_for_fused_assets(config):
    settings = config.registry.settings
    package_names = [x.split('.')[0] for x in OrderedSet(
        settings['website.dependencies'] + [config.root_package.__name__])]
    add_fused_asset_view(config, package_names, 'site.min.css')
    add_fused_asset_view(config, package_names, 'site.min.js')


def add_fused_asset_view(config, package_names, view_name):
    """
    Prepare view for asset that is assembled from many parts.
    Call this function after including your pyramid configuration callables.
    """
    LOG.debug('Generating %s' % view_name)
    file_name = view_name.replace('site', 'part')
    asset_parts = []
    for package_name in package_names:
        asset_spec = '%s:assets/%s' % (package_name, file_name)
        asset_path = get_asset_path(asset_spec)
        if not exists(asset_path):
            LOG.debug('_ %s' % asset_spec)
            continue
        asset_parts.append(open(asset_path).read().strip())
        LOG.debug('+ %s' % asset_spec)
    asset_content = '\n'.join(asset_parts)
    content_type = mimetypes.guess_type(view_name)[0]
    config.add_cached_view(
        lambda request: Response(
            asset_content, content_type=content_type, charset='utf-8'),
        name=view_name)


def get_asset_path(asset_spec):
    if ':' in asset_spec:
        asset_path = AssetResolver().resolve(asset_spec).abspath()
    else:
        asset_path = abspath(asset_spec)
    return asset_path
