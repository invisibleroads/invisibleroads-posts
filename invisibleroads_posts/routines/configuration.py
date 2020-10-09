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


def set_attribute(settings, class_registry, attribute_name, default, parse):
    for class_name, Class in class_registry.items():
        if class_name in (
            'EnumeratedBase',
            'RandomBase',
        ) or class_name.startswith('_'):
            continue
        prefix = getattr(Class, '__tablename__', class_name.casefold()) + '.'
        key = prefix + attribute_name
        value = set_default(settings, key, default, parse)
        setattr(Class, attribute_name.replace('.', '_'), value)
