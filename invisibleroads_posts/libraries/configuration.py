from invisibleroads_macros.iterable import set_default
from invisibleroads_macros.security import make_random_string


class Settings(dict):

    def set(self, settings, prefix, key, default=None, parse=None):
        value = set_default(settings, prefix + key, default, parse)
        self[key] = value
        return value


def fill_secrets(settings, prefix, secret_length=128):
    for k, v in settings.items():
        if not k.startswith(prefix):
            continue
        if k.endswith('.secret') and not v:
            settings[k] = make_random_string(secret_length)
