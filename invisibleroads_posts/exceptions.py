class InvisibleRoadsError(Exception):
    pass


class DataValidationError(ValueError, InvisibleRoadsError):
    pass
