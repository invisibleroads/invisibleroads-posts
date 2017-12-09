import mimetypes
from invisibleroads_macros.configuration import set_default
from invisibleroads_macros.iterable import OrderedSet
from invisibleroads_macros.log import get_log
from os import environ
from os.path import abspath, basename, exists
from paste.urlmap import URLMap
from pyramid.config import Configurator
from pyramid.path import AssetResolver
from pyramid.response import FileResponse, Response
from pyramid.settings import aslist
from six.moves.urllib.parse import urlparse as parse_url

from .libraries.cache import configure_cache, FUNCTION_CACHE
from .libraries.text import render_title
from .views import add_routes


L = get_log(__name__)


class InvisibleRoadsConfigurator(Configurator):

    def make_wsgi_app(self):
        app = super(InvisibleRoadsConfigurator, self).make_wsgi_app()

        settings = self.registry.settings
        base_url = settings['website.base_url']
        if base_url != '/':
            url_map = URLMap()
            url_map[base_url] = app
            app = url_map

        return app


def main(global_config, **settings):
    config = InvisibleRoadsConfigurator(settings=settings)
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
    # Define add_cached_static_view and add_cached_view
    http_expiration_time_in_seconds = set_default(
        settings, 'client_cache.http.expiration_time_in_seconds', 3600, int)
    config.add_directive(
        'add_cached_static_view',
        lambda config, *arguments, **keywords: config.add_static_view(
            *arguments, cache_max_age=http_expiration_time_in_seconds,
            **keywords))
    config.add_directive(
        'add_cached_view',
        lambda config, *arguments, **keywords: config.add_view(
            *arguments, http_cache=http_expiration_time_in_seconds,
            **keywords))
    # Define data_folder
    config.add_request_method(
        lambda request: settings['data.folder'], 'data_folder', reify=True)
    # Define website.dependencies
    settings['website.dependencies'] = []
    add_website_dependency(config)
    # Define website.environment
    for line in settings.get('website.environment', '').strip().splitlines():
        k, v = line.split()
        environ[k] = v
    # Define miscellaneous settings
    set_default(settings, 'website.root_assets', [
        'invisibleroads_posts:assets/favicon.ico',
        'invisibleroads_posts:assets/robots.txt',
    ], aslist)
    set_default(settings, 'website.version', '0.1')
    set_default(settings, 'website.name', 'InvisibleRoads')
    set_default(settings, 'website.owner', 'InvisibleRoads')
    set_default(settings, 'website.year', '2017')
    set_default(settings, 'website.brand_url', '/#')
    set_default(settings, 'website.base_url', '/', _prepare_base_url)
    set_default(
        settings, 'website.base_template',
        'invisibleroads_posts:templates/base.jinja2')
    set_default(
        settings, 'website.page_not_found_template',
        'invisibleroads_posts:templates/404.jinja2')


def configure_assets(config):
    settings = config.registry.settings
    config.add_cached_static_view(
        '_/invisibleroads-posts', 'invisibleroads_posts:assets')
    for asset_spec in settings['website.root_assets']:
        asset_path = get_asset_path(asset_spec)
        asset_name = basename(asset_path)
        config.add_cached_view(
            lambda request, x=asset_path: FileResponse(x, request), asset_name)


def configure_views(config):
    settings = config.registry.settings
    config.include('pyramid_jinja2')
    config.commit()
    config.get_jinja2_environment().globals.update({
        'website_version': settings['website.version'],
        'website_name': settings['website.name'],
        'website_owner': settings['website.owner'],
        'website_year': settings['website.year'],
        'base_template': settings['website.base_template'],
        'base_url': settings['website.base_url'],
        'brand_url': settings['website.brand_url'],
        'render_title': render_title,
    })
    add_routes(config)


def add_routes_for_fused_assets(config):
    settings = config.registry.settings
    package_names = OrderedSet(x.split('.')[0] for x in settings[
        'website.dependencies'] + [config.root_package.__name__])
    version = settings['website.version']
    add_fused_asset_view(config, package_names, 'site-%s.min.css' % version)
    add_fused_asset_view(config, package_names, 'site-%s.min.js' % version)


def add_fused_asset_view(config, package_names, view_name):
    """
    Prepare view for asset that is assembled from many parts.
    Call this function after including your pyramid configuration callables.
    """
    L.debug('Generating %s' % view_name)
    file_name = view_name.replace('site', 'part')
    asset_parts = []
    for package_name in package_names:
        asset_spec = '%s:assets/%s' % (package_name, file_name)
        asset_path = get_asset_path(asset_spec)
        if not exists(asset_path):
            L.debug('_ %s' % asset_spec)
            continue
        asset_parts.append(open(asset_path).read().strip())
        L.debug('+ %s' % asset_spec)
    asset_content = '\n'.join(asset_parts)
    content_type = mimetypes.guess_type(view_name)[0]
    config.add_cached_view(
        lambda request: Response(
            asset_content, content_type=content_type, charset='utf-8'),
        name=view_name)


def add_website_dependency(config, package_name=None):
    settings = config.registry.settings
    package_name = package_name or config.package_name
    settings['website.dependencies'].append(package_name)


def get_asset_path(asset_spec):
    if ':' in asset_spec:
        asset_path = AssetResolver().resolve(asset_spec).abspath()
    else:
        asset_path = abspath(asset_spec)
    return asset_path


def _prepare_base_url(x):
    path = parse_url(x).path.strip('/')
    return '/%s/' % path if path else '/'
