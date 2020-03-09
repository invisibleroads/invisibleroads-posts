from .exceptions import DataValidationError


def get_record_id(request, key):
    try:
        return request.matchdict[key]
    except KeyError:
        pass
    try:
        return request.params[key]
    except KeyError:
        pass
    try:
        return request.json_body[key]
    except KeyError:
        raise DataValidationError({key: 'is required'})
