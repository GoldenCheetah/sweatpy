from .exceptions import MissingDataException


def field_validations(fields):
    def field_validations_wrapper(func):
        def field_validations_decorator(*args, **kwargs):
            missing_fields = set(fields) - set(args[0])
            if missing_fields:
                raise MissingDataException(func, missing_fields)
            return func(*args, **kwargs)
        return field_validations_decorator
    return field_validations_wrapper
