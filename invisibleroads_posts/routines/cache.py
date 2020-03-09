from dogpile.cache.exception import RegionAlreadyConfigured


def configure_cache(settings, prefix, cache):
    if prefix + 'backend' not in settings:
        settings[prefix + 'backend'] = 'dogpile.cache.memory'
    try:
        cache.configure_from_config(settings, prefix)
    except RegionAlreadyConfigured:
        pass
