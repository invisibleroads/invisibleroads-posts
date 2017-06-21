from invisibleroads_macros.security import make_random_string


def fill_secrets(settings, prefix, secret_length=128):
    for k, v in settings.items():
        if not k.startswith(prefix):
            continue
        if k.endswith('.secret') and not v:
            settings[k] = make_random_string(secret_length)
