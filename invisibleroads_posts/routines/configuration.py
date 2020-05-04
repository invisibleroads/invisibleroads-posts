from functools import lru_cache
from invisibleroads_macros_configuration import (
    SECRET_LENGTH, fill_environment_variables, fill_extensions, fill_secrets,
    set_default)
from pyramid.paster import get_appsettings, setup_logging


@lru_cache(maxsize=None)
def load_filled_settings(configuration_path):
    setup_logging(configuration_path)
    settings = get_appsettings(configuration_path)
    return fill_settings(settings)


def fill_settings(settings):
    settings = fill_environment_variables(settings)
    settings = fill_secrets(settings, secret_length=set_default(
        settings, 'secret.length', SECRET_LENGTH, int))
    settings = fill_extensions(settings)
    return settings
