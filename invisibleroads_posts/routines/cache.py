def configure_cache(settings, prefix, cache):
    if prefix + 'backend' not in settings:
        settings[prefix + 'backend'] = 'dogpile.cache.memory'
    cache.configure_from_config(settings, prefix)
