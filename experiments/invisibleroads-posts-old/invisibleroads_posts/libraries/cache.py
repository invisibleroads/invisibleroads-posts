from dogpile.cache import make_region
from dogpile.cache.exception import RegionAlreadyConfigured


FUNCTION_CACHE = make_region()


def configure_cache(config, cache, prefix):
    settings = config.registry.settings
    if prefix + 'backend' not in settings:
        settings[prefix + 'backend'] = 'dogpile.cache.memory'
    try:
        cache.configure_from_config(settings, prefix)
    except RegionAlreadyConfigured:
        pass
