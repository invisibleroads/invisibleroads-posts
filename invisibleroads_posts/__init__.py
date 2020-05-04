from invisibleroads_macros_configuration import set_default
from os import environ

from .routines.cache import configure_cache
from .routines.configuration import fill_settings
from .variables import FUNCTION_CACHE


def includeme(config):
    configure_settings(config)
    configure_caches(config)


def configure_settings(config):
    settings = config.get_settings()
    settings = fill_settings(settings)

    if 'data.folder' in settings:
        config.add_request_method(
            lambda request: settings['data.folder'], 'data_folder', reify=True)

    for line in settings.get(
            'application.environment', '').strip().splitlines():
        k, v = line.split()
        environ[k] = v


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
