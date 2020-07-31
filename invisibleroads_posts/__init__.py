from invisibleroads_macros_configuration import set_default
from os import environ
from pyramid.events import NewResponse
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.settings import aslist

from .routines.cache import configure_cache
from .routines.configuration import fill_settings
from .variables import FUNCTION_CACHE


class CorsPreflightPredicate(object):

    def __init__(self, value, config):
        self.value = value

    def text(self):
        return 'cors_preflight = %s' % self.value

    phash = text

    def __call__(self, context, request):
        if not self.value:
            return False
        method = request.method
        headers = request.headers
        return (
            'OPTIONS' == method and
            'Origin' in headers and
            'Access-Control-Request-Method' in headers)


def includeme(config):
    configure_settings(config)
    configure_cross_origin_resource_sharing(config)
    configure_caches(config)


def configure_settings(config):
    settings = config.get_settings()
    fill_settings(settings)

    if 'data.folder' in settings:
        config.add_request_method(
            lambda request: settings['data.folder'], 'data_folder', reify=True)

    for line in settings.get(
            'application.environment', '').strip().splitlines():
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip()
        environ[k] = v


def configure_cross_origin_resource_sharing(config):
    settings = config.get_settings()
    allowed_origins = aslist(settings.get('cors.allowed_origins', '').lower())
    if not allowed_origins:
        return
    allowed_methods = aslist(settings.get('cors.allowed_methods', '').upper())
    allowed_headers = aslist(settings.get('cors.allowed_headers', '').title())

    def see_options(request):
        response = request.response
        response_headers = response.headers
        response_headers['Access-Control-Allow-Methods'] = ','.join(
            allowed_methods)
        response_headers['Access-Control-Allow-Headers'] = ','.join(
            allowed_headers)
        return response

    def set_cross_origin_resource_sharing(event):
        request = event.request
        request_headers = request.headers

        response = event.response
        response_headers = response.headers

        origin = request_headers.get('Origin', '')
        if origin.lower() not in allowed_origins:
            response.headers = {
                k: v for k, v in response_headers.items()
                if not k.startswith('Access-Control-')
            }
            return

        response_headers['Access-Control-Allow-Origin'] = origin
        if len(allowed_origins) > 1:
            response_headers['Vary'] = 'Origin'

    # https://gist.github.com/mmerickel/1afaf64154b335b596e4
    config.add_route_predicate('cors_preflight', CorsPreflightPredicate)
    config.add_route('corsPreflight', '/{all:.*}', cors_preflight=True)
    config.add_view(
        see_options, route_name='corsPreflight',
        permission=NO_PERMISSION_REQUIRED)
    config.add_subscriber(set_cross_origin_resource_sharing, NewResponse)


def configure_caches(config):
    settings = config.get_settings()

    # Configure client_cache
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

    # Configure server_cache
    configure_cache(settings, 'server_cache.function.', FUNCTION_CACHE)
