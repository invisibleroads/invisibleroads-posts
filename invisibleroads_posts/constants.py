from dogpile.cache import make_region


FUNCTION_CACHE = make_region()
SECRET_LENGTH = 128
