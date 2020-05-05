from functools import lru_cache
from invisibleroads_macros_configuration import (
    SECRET_LENGTH, fill_environment_variables, fill_extensions, fill_secrets,
    set_default)
from pyramid.paster import bootstrap, get_appsettings, setup_logging


@lru_cache(maxsize=None)
def load_bootstrapped_settings(configuration_path):
    'Load settings with full configuration'
    setup_logging(configuration_path)
    with bootstrap(configuration_path) as env:
        request = env['request']
    return request.registry.settings


@lru_cache(maxsize=None)
def load_filled_settings(configuration_path):
    setup_logging(configuration_path)
    settings = get_appsettings(configuration_path)
    fill_settings(settings)
    return settings


def fill_settings(settings):
    fill_environment_variables(settings)
    fill_secrets(settings, secret_length=set_default(
        settings, 'secret.length', SECRET_LENGTH, int))
    fill_extensions(settings)
