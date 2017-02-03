from .exceptions import MissingDataException


def requirements(columns=None, athlete=None):
    def requirements_wrapper(func):
        def requirements_decorator(*args, **kwargs):
            workout = args[0]
            missing_data = set()

            if columns:
                missing_data.update(set(columns) - set(list(workout)))

            if athlete:
                missing_data.update(
                    {i for i in athlete if not getattr(
                        workout._metadata['athlete'], i, None)})

            if missing_data:
                raise MissingDataException(func, missing_data)

            return func(*args, **kwargs)

        return requirements_decorator

    return requirements_wrapper
