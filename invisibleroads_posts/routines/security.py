from invisibleroads_macros_security import make_random_string

from .constants import (
    SECRET_LENGTH)


def fill_secrets(settings):
    for k, v in settings.items():
        if k.endswith('.secret') and not v:
            settings[k] = make_random_string(SECRET_LENGTH)
