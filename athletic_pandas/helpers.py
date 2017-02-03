from .exceptions import MissingDataException


def requirements(columns=None, athlete=None):
    def requirements_wrapper(func):
        def requirements_decorator(*args, **kwargs):
            wdf = args[0]
            missing_data = set()

            if columns:
                missing_data.update(set(columns) - set(list(wdf)))

            if athlete:
                missing_data.update(
                    {i for i in athlete if getattr(wdf.athlete, i, None) is None})

            if missing_data:
                raise MissingDataException(func, missing_data)

            return func(*args, **kwargs)

        return requirements_decorator

    return requirements_wrapper
