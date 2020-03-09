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


def includeme(config):
    configure_cache(config, FUNCTION_CACHE, 'server_cache.function.')
    configure_views(config)


def configure_settings(config):
    # Define add_cached_static_view and add_cached_view
    http_expiration_time_in_seconds = set_default(
        settings, 'client_cache.http.expiration_time_in_seconds', 3600, int)
    config.add_directive(
        'add_cached_view',
        lambda config, *arguments, **keywords: config.add_view(
            *arguments, http_cache=http_expiration_time_in_seconds,
            **keywords))
    # Define website.environment
    for line in settings.get('website.environment', '').strip().splitlines():
        k, v = line.split()
        environ[k] = v


def configure_views(config):
    settings = config.registry.settings
    add_routes(config)
