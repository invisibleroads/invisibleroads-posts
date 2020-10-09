from dogpile.cache import make_region


FUNCTION_CACHE = make_region()
POSTS_REGISTRY = {}
